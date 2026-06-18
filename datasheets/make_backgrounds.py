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

    # title must sit right of the meta block (which ends ~x=480)
    X_LEFT_LIMIT = 500
    max_w = TITLE_X_RIGHT - X_LEFT_LIMIT

    def pieces_for(px):
        semi = _load_font("Montserrat-SemiBold.ttf", px)
        bold = _load_font("Montserrat-Bold.ttf", px)
        ps = [(main + " ", semi), (suffix, bold)]
        if variant:
            ps.append((" " + variant, bold))
        return ps

    # auto-fit: start at the reference size (~54px caps) and shrink if too wide
    size = 76
    pieces = pieces_for(size)
    total = sum(_text_w(d, t, f) for t, f in pieces)
    if total > max_w:
        size = max(40, int(size * max_w / total))
        pieces = pieces_for(size)
        total = sum(_text_w(d, t, f) for t, f in pieces)

    # vertical centring: align cap centre to the original title band centre
    cap_bb = d.textbbox((0, 0), "M", font=pieces[0][1])
    cap_top, cap_h = cap_bb[1], cap_bb[3] - cap_bb[1]
    y_caps_top = TITLE_CY - cap_h // 2

    x = TITLE_X_RIGHT - total
    for t, f in pieces:
        bb = d.textbbox((0, 0), "M", font=f)
        d.text((x, y_caps_top - bb[1]), t, font=f, fill=WHITE)
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
