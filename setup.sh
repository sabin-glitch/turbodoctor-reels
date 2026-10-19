#!/bin/bash
# One-time setup per cloud session (~3-5 min): Python deps + offline ASR/TTS models. Safe to re-run.
set -e
M=${TD_MODELS:-/home/claude/models}; mkdir -p "$M"
pip install -q --break-system-packages sherpa-onnx soundfile scipy numpy opencv-python-headless playwright >/dev/null
ffmpeg -hide_banner -filters 2>/dev/null | grep -q vidstabdetect || echo "WARN: ffmpeg without vidstab - stab.sh will fall back to plain upscale"
REL=https://github.com/k2-fsa/sherpa-onnx/releases/download
get() { # $1 = release path, $2 = folder/file that must exist afterwards
  [ -e "$M/$2" ] && return; echo "downloading $1"
  case "$1" in *.tar.bz2) curl -sSL "$REL/$1" | tar -xj -C "$M" ;; *) curl -sSL -o "$M/$2" "$REL/$1" ;; esac; }
get asr-models/silero_vad.onnx silero_vad.onnx
get asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2 sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8
get asr-models/sherpa-onnx-whisper-turbo.tar.bz2 sherpa-onnx-whisper-turbo
# face detector for faces.py (OpenCV YuNet, MIT): graphics must never cover a face
mkdir -p "$M/face"; [ -s "$M/face/yunet.onnx" ] || curl -sSL -o "$M/face/yunet.onnx" https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
# licence-plate detector for plates.py (open-image-models, YOLOv9 ONNX; the model downloads itself from GitHub on first use)
pip install -q --break-system-packages open-image-models onnxruntime >/dev/null
python3 -c "import warnings; warnings.filterwarnings('ignore'); from open_image_models import create_detector; create_detector('yolo-v9-t-384-license-plate-end2end')" >/dev/null 2>&1 || echo "WARN: plate detector not ready - plates.py will retry the download"
rm -f "$M"/sherpa-onnx-whisper-turbo/turbo-encoder.onnx "$M"/sherpa-onnx-whisper-turbo/turbo-decoder.onnx "$M"/sherpa-onnx-whisper-turbo/*.weights 2>/dev/null || true
if [ "$1" = "--tts" ]; then mkdir -p "$M/tts"; [ -e "$M/tts/vits-piper-ro_RO-mihai-medium" ] || curl -sSL "$REL/tts-models/vits-piper-ro_RO-mihai-medium.tar.bz2" | tar -xj -C "$M/tts"; fi
echo "setup ok -> models in $M"
