"""Publică un videoclip explicativ direct în Biblioteca aplicației consilierilor (videoclipuri-turbodoctor.vercel.app).

Rulează în workflow-ul .github/workflows/publica-biblioteca.yml (cheia Supabase stă doar în secretele GitHub).
Pași: descarcă MP4-ul (doar de pe raw.githubusercontent.com/sabin-glitch/turbodoctor-reels, adică după publish_media.sh),
îl urcă în Storage la videos/biblioteca/<slug>.mp4, creează rândul în video_requests (pe numele adminului) și îl trece
pe „publicat”, ca istoricul să arate „noua -> publicat” făcut de Claude. Afișează linkul public pentru clienți.

Variabile: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (secret), VIDEO_URL, TITLU, SUBIECT, CONCLUZIE (opțional), DRY_RUN=1 (doar verifică).
"""
import json, os, random, re, shutil, string, subprocess, sys, tempfile, unicodedata, urllib.error, urllib.request

APP = "https://videoclipuri-turbodoctor.vercel.app"
ALLOWED = "https://raw.githubusercontent.com/sabin-glitch/turbodoctor-reels/"
MAX_BYTES = 48 * 1000 * 1000  # sub limita de 50 MB pe fișier a planului gratuit Supabase


def die(msg):
    print(f"EROARE: {msg}", file=sys.stderr); sys.exit(1)


def slugify(s):  # la fel ca în aplicație (AdminCerere.tsx)
    base = unicodedata.normalize("NFD", s)
    base = "".join(c for c in base if not unicodedata.combining(c)).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")[:50]
    return f"{base or 'video'}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"


def req(method, url, key, body=None, headers=None, raw=None):
    h = {"apikey": key, "Authorization": f"Bearer {key}"}
    h.update(headers or {})
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    if body is not None: h.setdefault("Content-Type", "application/json")
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            txt = resp.read().decode() or "null"
            return json.loads(txt) if txt.strip().startswith(("[", "{", "null")) else txt
    except urllib.error.HTTPError as e:
        die(f"{method} {url.split('?')[0]} -> HTTP {e.code}: {e.read().decode()[:400]}")


def main():
    env = os.environ
    video_url, titlu, subiect = env.get("VIDEO_URL", "").strip(), env.get("TITLU", "").strip(), env.get("SUBIECT", "").strip()
    concluzie = env.get("CONCLUZIE", "").strip() or "Videoclip publicat direct în bibliotecă."
    dry = env.get("DRY_RUN", "") in ("1", "true", "da")
    if not video_url.startswith(ALLOWED) or not video_url.lower().endswith(".mp4"):
        die(f"VIDEO_URL trebuie să fie un .mp4 de pe {ALLOWED} (linkul dat de publish_media.sh)")
    if len(titlu) < 5 or len(subiect) < 10:
        die("TITLU (min. 5 caractere) și SUBIECT (min. 10 caractere) sunt obligatorii")

    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    with urllib.request.urlopen(video_url, timeout=300) as r, open(tmp, "wb") as f:
        f.write(r.read())
    size = os.path.getsize(tmp); head = open(tmp, "rb").read(12)
    if head[4:8] != b"ftyp": die("fișierul descărcat nu e MP4")
    if size > MAX_BYTES:  # re-encodez la un bitrate care încape, păstrând rezoluția
        if not shutil.which("ffmpeg"): die(f"videoclipul are {size / 1e6:.1f} MB (limita 48 MB) și nu am ffmpeg ca să-l micșorez")
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", tmp]).decode())
        kbps = int(MAX_BYTES * 8 * 0.92 / dur / 1000) - 160
        small = tmp[:-4] + "_mic.mp4"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-c:v", "libx264", "-preset", "medium", "-b:v", f"{kbps}k",
                        "-maxrate", f"{int(kbps * 1.5)}k", "-bufsize", f"{kbps * 2}k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                        "-movflags", "+faststart", small], check=True)
        print(f"Re-encodat: {size / 1e6:.1f} MB -> {os.path.getsize(small) / 1e6:.1f} MB"); tmp, size = small, os.path.getsize(small)
        if size > MAX_BYTES: die(f"tot are {size / 1e6:.1f} MB după re-encodare")
    slug = slugify(titlu); path = f"biblioteca/{slug}.mp4"
    print(f"Videoclip: {size / 1e6:.1f} MB · titlu: {titlu} · slug: {slug}")
    if dry:
        print("DRY_RUN: nu urc nimic."); return

    sb, key = env.get("SUPABASE_URL", "").rstrip("/"), env.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not sb or not key: die("lipsește secretul SUPABASE_SERVICE_ROLE_KEY în GitHub (Settings → Secrets → Actions)")
    admin = req("GET", f"{sb}/rest/v1/profiles?rol=eq.admin&activ=eq.true&select=id&order=created_at.asc&limit=1", key)
    if not admin: die("nu găsesc niciun cont de admin activ în aplicație")
    req("POST", f"{sb}/storage/v1/object/videos/{path}", key, raw=open(tmp, "rb").read(),
        headers={"Content-Type": "video/mp4", "cache-control": "max-age=31536000"})
    row = req("POST", f"{sb}/rest/v1/video_requests", key, body={
        "consilier_id": admin[0]["id"], "subiect": subiect, "concluzie_client": concluzie,
        "speta": "Încărcat direct în bibliotecă din contul de producție, fără cerere de la un consilier.",
        "titlu": titlu, "slug": slug, "video_path": path}, headers={"Prefer": "return=representation"})
    rid = row[0]["id"]
    req("PATCH", f"{sb}/rest/v1/video_requests?id=eq.{rid}", key, body={"status": "publicat"}, headers={"Prefer": "return=minimal"})
    link = f"{APP}/v/{slug}"
    print(f"PUBLICAT în bibliotecă: {link}")
    if env.get("GITHUB_STEP_SUMMARY"):
        open(env["GITHUB_STEP_SUMMARY"], "a").write(f"### Publicat în bibliotecă\n\n**{titlu}**\n\nLink pentru clienți: {link}\n")


if __name__ == "__main__":
    main()
