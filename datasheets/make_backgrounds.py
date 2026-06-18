"""Build per-product full-page letterhead backgrounds.

Starts from the reference Lateral Repairs letterhead (extracted from the
supplied FORCE TDS PDF) so the logo, "TECHNICAL DATA SHEET" block, grey bar,
magenta contact footer and watermark are pixel-identical to the reference.
Only the product title in the grey bar is re-rendered (Montserrat) per product.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
BG_SRC = os.path.join(ASSETS, "letterhead.png")   # extracted reference bg
BG_DIR = os.path.join(ASSETS, "bg")
MONT = os.path.join(ASSETS, "fonts")
os.makedirs(BG_DIR, exist_ok=True)

GREY = (198, 197, 197)
WHITE = (255, 255, 255)

# grey-bar / title geometry (in the 1414x2000 letterhead)
BAR_TOP, BAR_BOT = 246, 413
TITLE_X_RIGHT = 1244
TITLE_Y0, TITLE_Y1 = 304, 358            # cap band of original title
TITLE_CY = (TITLE_Y0 + TITLE_Y1) // 2

# products: (slug, main, suffix, variant)
TITLES = [
    ("pro-40", "MULTIline", "PRO", "4.0 mm"),
    ("pro-45", "MULTIline", "PRO", "4.5 mm"),
    ("flex",   "MULTIline", "FLEX", ""),
    ("core",   "MULTIline", "CORE", ""),
    ("force",  "MULTIline", "FORCE", ""),
    ("force-rf", "MULTIline", "FORCE", "RF"),
    ("force-uv", "MULTIline", "FORCE", "UV"),
]


def _load_font(name, px):
    return ImageFont.truetype(os.path.join(MONT, name), px)


def _text_w(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0]


def build_one(src, slug, main, suffix, variant):
    im = src.copy()
    d = ImageDraw.Draw(im)
    # erase the original baked title (right part of the grey bar)
    d.rectangle([588, BAR_TOP + 2, 1300, BAR_BOT - 2], fill=GREY)

    # fonts sized so cap height matches the original (~54 px)
    semi = _load_font("Montserrat-SemiBold.ttf", 76)
    bold = _load_font("Montserrat-Bold.ttf", 76)

    # build pieces right-to-left: main(SemiBold) + " " + suffix(Bold)[+ " "+variant(Bold)]
    pieces = [(main + " ", semi), (suffix, bold)]
    if variant:
        pieces.append((" " + variant, bold))

    total = sum(_text_w(d, t, f) for t, f in pieces)
    x = TITLE_X_RIGHT - total
    # vertical: align cap tops to TITLE_Y0 (use ascent offset)
    for t, f in pieces:
        # textbbox top offset to seat caps at TITLE_Y0
        bb = d.textbbox((0, 0), t.strip() or "M", font=f)
        y = TITLE_Y0 - bb[1]
        d.text((x, y), t, font=f, fill=WHITE)
        x += _text_w(d, t, f)
    im.save(os.path.join(BG_DIR, f"{slug}.png"))
    return im


def main():
    src = Image.open(BG_SRC).convert("RGB")
    for slug, main_t, suffix, variant in TITLES:
        build_one(src, slug, main_t, suffix, variant)
        print("bg:", slug)


if __name__ == "__main__":
    main()
