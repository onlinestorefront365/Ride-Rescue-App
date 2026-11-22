"""Build the Stage 1-2 exploration package.

    python brand/src/build_stage2.py      # writes SVGs + board HTML
    node   brand/src/render.js            # renders PNG size tests + boards

Outputs go to brand/exploration/stage-2/.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import (CONCEPTS, to_d, bounds, poly, rect, diff, inter, H, BOWL, T,
                      concept_a_tandem, concept_b_lane, concept_c_route)
from wordmark import text_path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "exploration", "stage-2")

NAVY, LIME, WHITE, AMBER, GRAPHITE, GRAY = "#14283D", "#B9E532", "#F5F6F2", "#D99B67", "#252A30", "#87929D"

WORD_CAP = H * 0.42          # wordmark cap height relative to mark height
WORD_GAP = 22                # space between mark and wordmark (mark units)
WORD = dict(weight=800, tracking=0.06)

SIZES = [1024, 512, 128, 64, 32]


def svg(viewbox, body, w=None, h=None):
    size = f' width="{w}" height="{h}"' if w else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}"{size}>'
            f'{body}</svg>\n')


def vb(b, pad=0):
    x0, y0, x1, y1 = b
    return f"{x0 - pad:.2f} {y0 - pad:.2f} {x1 - x0 + 2 * pad:.2f} {y1 - y0 + 2 * pad:.2f}"


def negative_space(key, mark):
    """The concept's key negative-space feature, for construction diagrams."""
    if key == "b-lane":
        from geometry import lane_road, LANE_STAGE2
        return lane_road(**LANE_STAGE2)
    if key == "a-tandem":
        hp = poly((7.2, 0), (46, 0), (46, H), (49.2, H))
        return inter(diff(rect(0, 0, 46, H), mark), hp)
    return None


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def lockup(mark, mark_fill, word_fill):
    word, ww = text_path("RIDE RESCUE", WORD_CAP, **WORD)
    x0, y0, x1, y1 = bounds(mark)
    ox = x1 + WORD_GAP
    oy = (H - WORD_CAP) / 2
    body = (f'<path fill="{mark_fill}" d="{to_d(mark)}"/>'
            f'<path fill="{word_fill}" transform="translate({ox:.2f} {oy:.2f})" d="{to_d(word)}"/>')
    return body, (x0, y0, ox + ww, y1)


def app_tile(mark, size_units=100):
    """Full-bleed square tile (stores apply their own corner mask)."""
    x0, y0, x1, y1 = bounds(mark)
    w, h = x1 - x0, y1 - y0
    target_w = size_units * 0.60
    s = target_w / w
    tx = (size_units - w * s) / 2 - x0 * s
    ty = (size_units - h * s) / 2 - y0 * s
    return (f'<rect width="{size_units}" height="{size_units}" fill="{NAVY}"/>'
            f'<path fill="{LIME}" transform="translate({tx:.3f} {ty:.3f}) scale({s:.4f})" d="{to_d(mark)}"/>')


def main():
    manifest = {}
    for key, (name, fn) in CONCEPTS.items():
        mark = fn()
        b = bounds(mark)
        d = to_d(mark)
        folder = os.path.join(OUT, key)
        files = {}

        # 1. master mark, single compound path, transparent background
        for label, fill in (("navy", NAVY), ("lime", LIME), ("white", WHITE), ("black", "#000000")):
            fname = f"{key}-mark-{label}.svg"
            write(os.path.join(folder, fname), svg(vb(b), f'<path fill="{fill}" d="{d}"/>'))
            files[f"mark-{label}"] = fname

        # 2. horizontal lockups
        body, lb = lockup(mark, NAVY, NAVY)
        write(os.path.join(folder, f"{key}-lockup-light.svg"), svg(vb(lb), body))
        body, lb = lockup(mark, LIME, WHITE)
        write(os.path.join(folder, f"{key}-lockup-dark.svg"), svg(vb(lb), body))
        files["lockup-light"] = f"{key}-lockup-light.svg"
        files["lockup-dark"] = f"{key}-lockup-dark.svg"

        # 3. app tile master (rendered to PNG at each test size by render.js)
        write(os.path.join(folder, f"{key}-app-tile.svg"), svg("0 0 100 100", app_tile(mark)))
        files["app-tile"] = f"{key}-app-tile.svg"

        # 4. construction diagram
        x0, y0, x1, y1 = b
        ns = negative_space(key, mark)
        guides = "".join(
            f'<line x1="{x0 - 6}" x2="{x1 + 6}" y1="{y}" y2="{y}" stroke="{AMBER}" stroke-width="0.35" stroke-dasharray="1.5 1"/>'
            for y in (0, T, BOWL - T, BOWL, H))
        ns_svg = f'<path fill="{LIME}" d="{to_d(ns)}"/>' if ns else ""
        route = ""
        if key == "c-route":
            route = (f'<polyline fill="none" stroke="{AMBER}" stroke-width="0.6" stroke-linejoin="round" '
                     f'points="8.25,58.75 8.25,5.25 22.25,5.25 22.25,34 20.25,34 48.25,58.75 48.25,5.25 62.25,5.25 62.25,34 60.25,34 78.25,58.75"/>')
        cons = (f'<path fill="{NAVY}" fill-opacity="0.12" stroke="{NAVY}" stroke-width="0.4" d="{d}"/>'
                f'{ns_svg}{guides}{route}'
                f'<text x="{x1 + 7}" y="1.5" font-size="3" fill="{GRAY}" font-family="sans-serif">cap 64</text>'
                f'<text x="{x1 + 7}" y="{BOWL + 1}" font-size="3" fill="{GRAY}" font-family="sans-serif">bowl {BOWL}</text>'
                f'<text x="{x1 + 7}" y="{H + 1}" font-size="3" fill="{GRAY}" font-family="sans-serif">baseline</text>')
        write(os.path.join(folder, f"{key}-construction.svg"),
              svg(f"{x0 - 8} {y0 - 6} {x1 - x0 + 34} {y1 - y0 + 12}", cons))
        files["construction"] = f"{key}-construction.svg"

        manifest[key] = {"name": name, "files": files,
                         "width": round(x1 - x0, 2), "height": round(y1 - y0, 2)}

    write(os.path.join(OUT, "manifest.json"), json.dumps({"sizes": SIZES, "concepts": manifest}, indent=2))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
