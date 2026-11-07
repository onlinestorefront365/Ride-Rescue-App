"""Copy identity v2 assets into the website (assets/img) in web-ready form.

    python brand/src/site_assets.py
    node   brand/src/render_site_icons.js   # favicon PNG, apple-touch-icon, social image
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import to_d, bounds
from rr2 import rr_mark

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = os.path.join(ROOT, "assets", "img")
ID = os.path.join(ROOT, "brand", "identity")
CARBON, WHITE, BLUE = "#111315", "#FFFFFF", "#087FFF"

# old Lane-era files that the v2 site no longer uses
STALE = ["logo-horizontal-dark.svg", "logo-horizontal-navy.svg", "rr-monogram-lime.svg", "pattern-road-tile.svg"]


def tile(size, fill_ratio, rx):
    """White RR micro mark centred on a Carbon tile."""
    mark = rr_mark()
    x0, y0, x1, y1 = bounds(mark)
    w, h = x1 - x0, y1 - y0
    s = size * fill_ratio / w
    tx, ty = (size - w * s) / 2 - x0 * s, (size - h * s) / 2 - y0 * s
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
            f'<rect width="{size}" height="{size}" rx="{rx}" fill="{CARBON}"/>'
            f'<path fill="{WHITE}" transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})" d="{to_d(mark)}"/></svg>\n')


def main():
    os.makedirs(IMG, exist_ok=True)
    for f in STALE:
        p = os.path.join(IMG, f)
        if os.path.exists(p):
            os.remove(p)
    for src, dst in (("logo/svg/ride-rescue-horizontal-compact-dark.svg", "logo-compact-dark.svg"),
                     ("logo/svg/emblem-dark.svg", "emblem-dark.svg"),
                     ("logo/svg/ride-rescue-stacked-dark.svg", "logo-stacked-dark.svg"),
                     ("graphics/carbon-fibre-tile.svg", "carbon-fibre-tile.svg"),
                     ("graphics/ridge-band-raised.svg", "ridge-band.svg"),
                     ("graphics/road-line-blue.svg", "road-line-blue.svg"),
                     ("icons/sprite.svg", "icons.svg")):
        shutil.copy(os.path.join(ID, src), os.path.join(IMG, dst))
    with open(os.path.join(IMG, "favicon.svg"), "w") as f:
        f.write(tile(64, 0.86, 12))
    with open(os.path.join(IMG, "app-tile-master.svg"), "w") as f:
        f.write(tile(180, 0.72, 0))
    print("site assets written to", IMG)


if __name__ == "__main__":
    main()
