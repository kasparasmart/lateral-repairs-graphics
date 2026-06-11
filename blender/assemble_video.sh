#!/usr/bin/env bash
# Assemble rendered frames into the final promo video.
# - 24 fps, frames in /tmp/frames/frame_0001.png .. frame_0200.png
# - fades in from black, then holds the final frame as a still picture
set -euo pipefail

FRAMES_DIR="${1:-/tmp/frames}"
OUT="${2:-renders/lateral_repairs_promo.mp4}"

mkdir -p "$(dirname "$OUT")"
ffmpeg -y -framerate 24 -i "$FRAMES_DIR/frame_%04d.png" \
  -vf "tpad=stop_mode=clone:stop_duration=3.5,fade=t=in:st=0:d=0.5,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -movflags +faststart \
  "$OUT"
echo "Wrote $OUT"
