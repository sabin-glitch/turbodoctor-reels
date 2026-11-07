"""ElevenLabs text-to-speech for one narrator job (runs on GitHub Actions, where api.elevenlabs.io is reachable).
Usage: elevenlabs_tts.py <job.json> <out_dir>
job.json: {"voice_id": "...", "model_id": "eleven_multilingual_v2", "language_code": "ro", "output_format": "mp3_44100_128",
           "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": true},
           "lines": [{"id": "00", "text": "..."}, ...]}
Writes <out_dir>/<id>.mp3 for every line and <out_dir>/<job>.json (text + bytes per line). Lines already present are regenerated."""
import json, os, sys, time, requests

job_path, out = sys.argv[1], sys.argv[2]
job = json.load(open(job_path, encoding="utf-8")); os.makedirs(out, exist_ok=True)
key = os.environ["ELEVENLABS_API_KEY"]
voice = job["voice_id"]; model = job.get("model_id", "eleven_multilingual_v2"); fmt = job.get("output_format", "mp3_44100_128")
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format={fmt}"
manifest = []
for L in job["lines"]:
    body = {"text": L["text"], "model_id": model}
    if job.get("language_code"): body["language_code"] = job["language_code"]
    if job.get("voice_settings"): body["voice_settings"] = job["voice_settings"]
    if job.get("seed") is not None: body["seed"] = job["seed"]
    for attempt in range(4):
        r = requests.post(url, headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"}, json=body, timeout=120)
        if r.status_code == 200: break
        print(f"[{L['id']}] HTTP {r.status_code}: {r.text[:200]}"); time.sleep(3 * (attempt + 1))
    r.raise_for_status()
    p = f"{out}/{L['id']}.mp3"; open(p, "wb").write(r.content)
    manifest.append({"id": L["id"], "text": L["text"], "bytes": len(r.content)}); print(f"[{L['id']}] {len(r.content)} B  {L['text'][:60]}")
json.dump({"voice_id": voice, "model_id": model, "lines": manifest}, open(f"{out}/{os.path.basename(job_path)}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done", len(manifest), "lines")
