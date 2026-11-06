"""Copy brand assets into the website (assets/img) in web-ready form.

    python brand/src/site_assets.py
    node   brand/src/render_site_icons.js   # favicon PNG + apple-touch-icon
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import lane_mark, lane_road, LANE_MASTER, LANE_SMALL, to_d, bounds
import icons as icon_mod

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = os.path.join(ROOT, "assets", "img")
ID = os.path.join(ROOT, "brand", "identity")
NAVY, LIME = "#14283D", "#B9E532"


def tile(mark, size, fill_ratio, rx):
    x0, y0, x1, y1 = bounds(mark)
    w, h = x1 - x0, y1 - y0
    s = size * fill_ratio / w
    tx, ty = (size - w * s) / 2 - x0 * s, (size - h * s) / 2 - y0 * s
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
            f'<rect width="{size}" height="{size}" rx="{rx}" fill="{NAVY}"/>'
            f'<path fill="{LIME}" transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})" d="{to_d(mark)}"/></svg>\n')


def main():
    os.makedirs(IMG, exist_ok=True)
    # logos used by the site
    for src, dst in (("ride-rescue-horizontal-dark.svg", "logo-horizontal-dark.svg"),
                     ("ride-rescue-horizontal-navy.svg", "logo-horizontal-navy.svg"),
                     ("rr-monogram-lime.svg", "rr-monogram-lime.svg")):
        shutil.copy(os.path.join(ID, "logo", "svg", src), os.path.join(IMG, dst))
    # favicon: small-size cut on a rounded navy tile
    with open(os.path.join(IMG, "favicon.svg"), "w") as f:
        f.write(tile(lane_mark(**LANE_SMALL), 64, 0.84, 12))
    # full-bleed tile masters for PNG icons (platforms apply their own corner mask)
    with open(os.path.join(IMG, "app-tile-master.svg"), "w") as f:
        f.write(tile(lane_mark(**LANE_MASTER), 180, 0.66, 0))
    shutil.copy(os.path.join(ID, "graphics", "pattern-road-tile.svg"), os.path.join(IMG, "pattern-road-tile.svg"))
    # icon sprite
    shutil.copy(os.path.join(ID, "icons", "sprite.svg"), os.path.join(IMG, "icons.svg"))
    print("site assets written to", IMG)


if __name__ == "__main__":
    main()
