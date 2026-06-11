# Lateral Repairs — Graphics

Promo video and related graphics for Lateral Repairs, built entirely with
Blender (headless, via the `bpy` Python module) and ffmpeg.

## Promo video

`renders/lateral_repairs_promo.mp4` — ~12 s, 960x540, 24 fps.

Storyboard:

1. A CCTV-style camera travels through a pipe while a glowing applicator
   ring ahead of it lays a fresh resin liner on the pipe wall (UV-cure
   glow band at the resin front).
2. The camera flies out of the pipe mouth and arcs around to face it.
3. The Lateral Repairs logo launches out of the pipe, spins and settles
   centered in frame.
4. The shot becomes a still picture with **MANUFACTURING PERFECTION**
   written at the bottom.

## Rebuilding

Requirements: Python 3.11, `pip install bpy`, `ffmpeg`.

```bash
cd blender
python3 promo_video.py --render 1 200   # renders frames to /tmp/frames (slow on CPU)
./assemble_video.sh /tmp/frames ../renders/lateral_repairs_promo.mp4
```

`promo_video.py` also saves the generated scene to
`/tmp/lateral_repairs_promo.blend`, which can be opened in the Blender UI
for further editing.
