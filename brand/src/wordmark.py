"""Ride Rescue — wordmark outlines.

Sets RIDE RESCUE from Manrope (SIL Open Font License) at a fixed weight,
applies brand tracking and manual pair spacing, and converts the result to
outlines so the wordmark never depends on an installed font.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.transformPen import TransformPen
from pathops import Path, op, PathOp

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Manrope-Variable.ttf")

_cache = {}


def _font(weight):
    if weight not in _cache:
        f = TTFont(FONT)
        _cache[weight] = instantiateVariableFont(f, {"wght": weight})
    return _cache[weight]


def _place(path, k, dx):
    out = Path()
    path.draw(TransformPen(out.getPen(), (k, 0, 0, k, dx, 0)))
    return out


def text_path(text, cap_height, weight=800, tracking=0.08, pairs=None, font_path=None, custom_r=False):
    """Return (Path, width) for `text` scaled so caps are `cap_height` tall.

    tracking is in em (0.08 = +80 units/1000). `pairs` adjusts spacing
    between specific letter pairs, also in em, e.g. {"RI": -0.01}.
    Baseline sits at y = cap_height, top of caps at y = 0 (SVG coordinates).
    """
    if font_path:
        f = instantiateVariableFont(TTFont(font_path), {"wght": weight})
    else:
        f = _font(weight)
    upm = f["head"].unitsPerEm
    cap = f["OS/2"].sCapHeight
    s = cap_height / cap
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    pairs = pairs or {}
    out = Path()
    x = 0.0
    prev = None
    for ch in text:
        if prev is not None:
            x += pairs.get(prev + ch, 0) * upm * s
        gname = cmap[ord(ch)]
        adv = hmtx[gname][0]
        if ch == "R" and custom_r:
            # Monogram-derived R: same 64/12 construction as the Lane mark,
            # scaled to cap height, with Manrope's R side-bearings.
            from geometry import brand_r, H as MARK_H
            r_path, r_w = brand_r()
            k = cap_height / MARK_H
            lsb = 140 * s
            out = op(out, _place(r_path, k, x + lsb), PathOp.UNION)
            x += lsb + r_w * k + 80 * s + tracking * upm * s
            prev = ch
            continue
        if ch != " ":
            # font units are y-up; flip into SVG y-down with baseline at cap_height
            pen = TransformPen(out.getPen(), (s, 0, 0, -s, x, cap_height))
            gs[gname].draw(pen)
        x += adv * s + tracking * upm * s
        prev = ch
    width = x - tracking * upm * s
    clean = op(out, Path(), PathOp.UNION)  # resolve overlapping contours
    return clean, width
