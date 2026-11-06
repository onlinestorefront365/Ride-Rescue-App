"""Ride Rescue identity v2 — RR monogram, gear, mountain and swoosh geometry.

Industrial italic construction:
  - 64-unit cap height, 16-unit stroke (X), 46-unit bowl
  - letters drawn upright from rounded-square parts, then slanted 12 degrees
    to match Saira Italic, the wordmark typeface
  - every exported shape is boolean-unioned into clean compound paths
"""
import math
from pathops import Path
from fontTools.pens.transformPen import TransformPen
from geometry import poly, rect, circle, union, diff, inter, leg, K, to_d, bounds

H = 64          # cap height
X = 16          # stroke = system unit (0.25 H, matches Saira Italic 800)
BOWL = 46
W = 50          # R width (upright)
SLANT = math.tan(math.radians(12))


def xform(path, a, b, c, d, e, f):
    out = Path()
    path.draw(TransformPen(out.getPen(), (a, b, c, d, e, f)))
    return out


def italic(path, base=H):
    """Slant 12 degrees about the baseline (y-down: top moves right)."""
    return xform(path, 1, 0, -SLANT, 1, SLANT * base, 0)


def move(path, dx=0, dy=0):
    return xform(path, 1, 0, 0, 1, dx, dy)


def scale(path, s, cx=0, cy=0):
    return xform(path, s, 0, 0, s, cx - s * cx, cy - s * cy)


def rrect(x0, y0, x1, y1, tl=0, tr=0, br=0, bl=0):
    """Rectangle with an independent radius on each corner."""
    p = Path()
    p.moveTo(x0 + tl, y0)
    p.lineTo(x1 - tr, y0)
    if tr:
        p.cubicTo(x1 - tr + K * tr, y0, x1, y0 + tr - K * tr, x1, y0 + tr)
    p.lineTo(x1, y1 - br)
    if br:
        p.cubicTo(x1, y1 - br + K * br, x1 - br + K * br, y1, x1 - br, y1)
    p.lineTo(x0 + bl, y1)
    if bl:
        p.cubicTo(x0 + bl - K * bl, y1, x0, y1 - bl + K * bl, x0, y1 - bl)
    p.lineTo(x0, y0 + tl)
    if tl:
        p.cubicTo(x0, y0 + tl - K * tl, x0 + tl - K * tl, y0, x0 + tl, y0)
    p.close()
    return p


def r_upright(t=X, w=W, bowl=BOWL, r_out=16, r_in=4):
    """Squared industrial R, upright, origin at top-left, baseline at y = H."""
    stem = rect(0, 0, t, H)
    outer = rrect(0, 0, w, bowl, tr=r_out, br=r_out)
    inner = rrect(t, t, w - t, bowl - t, tr=r_in, br=r_in)
    bw = diff(outer, inner)
    lg = leg(w - t - 6, bowl - t / 2, w - t / 2 - 1, H, t)
    lg = inter(lg, rect(0, bowl - t, w + 4, H))
    return union(stem, bw, lg)


def r_italic(**kw):
    return italic(r_upright(**kw))


# ------------------------------------------------------------- RR options
def rr_pair(gap=6):
    """Two R's side by side."""
    r1 = r_upright()
    r2 = move(r_upright(), W + gap)
    return italic(union(r1, r2))


def rr_interlock(overlap=10, knock=3):
    """Second R overlaps the first R's leg; a knock-out gap keeps both legible."""
    r1 = r_upright()
    r2 = move(r_upright(), W - overlap)
    halo = _offset_rect_halo(r2, knock)
    return italic(union(diff(r1, halo), r2))


def rr_drive(gap=5, run=14, lift=7):
    """First R's leg kicks forward into a road line that runs on under the
    second R and past it: the onward trajectory."""
    r1 = r_upright()
    r2 = move(r_upright(), W + gap)
    leg_l = W - X - 1                       # left edge of R1's leg at the baseline
    tip = 2 * W + gap + run                 # where the road line ends, past R2
    road = poly((leg_l, H - lift), (tip, H - 0.6), (tip, H), (leg_l, H))
    return italic(union(r1, r2, road))


def _offset_rect_halo(path, d):
    """Cheap outward offset: union of the path shifted in 8 directions."""
    parts = [path]
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        parts.append(move(path, d * math.cos(a), d * math.sin(a)))
    return union(*parts)


# ------------------------------------------------------------- micro mark
def rr_mark():
    """The approved RR monogram (Drive, long run)."""
    return rr_drive(run=26, lift=9)


# ------------------------------------------------------------- emblem parts
def gear(n=9, r_tip=100, r_root=85, r_hole=68, tip_frac=0.34, root_frac=0.5):
    """Gear ring centred on the origin. Teeth are trapezoids with flat tips."""
    body = circle(0, 0, r_root)
    step = 2 * math.pi / n
    teeth = []
    for i in range(n):
        a = -math.pi / 2 + i * step          # first tooth points straight up
        hr, ht = step * root_frac / 2, step * tip_frac / 2
        pts = [(math.cos(a - hr) * (r_root - 2), math.sin(a - hr) * (r_root - 2)),
               (math.cos(a - ht) * r_tip, math.sin(a - ht) * r_tip),
               (math.cos(a + ht) * r_tip, math.sin(a + ht) * r_tip),
               (math.cos(a + hr) * (r_root - 2), math.sin(a + hr) * (r_root - 2))]
        teeth.append(poly(*pts))
    return diff(union(body, *teeth), circle(0, 0, r_hole))


def rotate(path, deg, cx=0, cy=0):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return xform(path, c, s_, -s_, c, cx - c * cx + s_ * cy, cy - s_ * cx - c * cy)


def twelve_point(r, rot=0):
    """12-point (double-hex) socket opening: two hexagons 30 degrees apart."""
    def hexagon(off):
        return poly(*[(r * math.cos(math.radians(off + k * 60)), r * math.sin(math.radians(off + k * 60))) for k in range(6)])
    return union(hexagon(rot), hexagon(rot + 30))


WRENCH = dict(angle=135, r_head=100, ring=14, seam=2.2, r_12=72, length=218, neck=74, shank=42,
              r_open=43, jaw=34, jaw_tilt=15)


def wrench(angle=135, r_head=100, ring=14, seam=2.2, r_12=72, length=250, neck=74, shank=42,
           r_open=46, jaw=36, jaw_tilt=15):
    """12-point ratcheting combination wrench; box-end head centred on the origin.

    Box end: outer head ring, a thin seam, then the ratchet ring with a
    12-point opening (the seam is what reads as 'ratcheting').
    Shank: flares into the head like a forged neck, then runs straight.
    Open end: jaw tilted 15 degrees, the classic combination-wrench cue.
    angle: handle direction in screen degrees (135 = lower left).
    """
    r0 = r_head * 0.72
    shank_poly = poly((r0, -neck / 2), (r_head + 22, -shank / 2), (length - r_open * 0.6, -shank / 2 * 0.94),
                      (length - r_open * 0.6, shank / 2 * 0.94), (r_head + 22, shank / 2), (r0, neck / 2))
    open_head = circle(length, 0, r_open)
    slot = union(rect(length - 4, -jaw / 2, length + r_open + 10, jaw / 2), circle(length - 4, 0, jaw / 2))
    slot = rotate(slot, jaw_tilt, length, 0)
    open_end = diff(open_head, slot)
    body = union(circle(0, 0, r_head), shank_poly, open_end)
    body = rotate(body, angle)
    outer = diff(body, circle(0, 0, r_head - ring))
    ratchet = diff(circle(0, 0, r_head - ring - seam), twelve_point(r_12))
    return union(outer, ratchet)


def mountain(r_clip=62, gap=3.2, clip=None):
    """Ridge with snow caps, separated by a jagged gap. Returns (rock, snow).
    clip: optional Path the ridge is trimmed to (defaults to a circle of r_clip)."""
    ridge = poly((-62, 12), (-38, -24), (-28, -16), (-6, -56), (12, -30), (26, -42), (62, 4), (62, 40), (-62, 40))
    ridge = inter(ridge, clip if clip is not None else circle(0, 0, r_clip))
    jag = [(-62, -34), (-40, -34), (-30, -28), (-22, -30), (-12, -22), (-4, -36), (6, -26), (14, -32),
           (20, -24), (30, -32), (40, -22), (62, -10)]
    above = poly((-80, -90), (80, -90), *[(x, y) for x, y in reversed(jag)][:0], (80, jag[-1][1]),
                 *reversed(jag), (-80, jag[0][1]))
    above_gap = poly((-80, -90), (80, -90), (80, jag[-1][1] + gap),
                     *[(x, y + gap) for x, y in reversed(jag)], (-80, jag[0][1] + gap))
    snow = inter(ridge, above)
    rock = diff(ridge, above_gap)
    return rock, snow


def swoosh(cx=0, cy=34, r=94, d=7.5):
    """Tapered crescent: thickest at upper left, fading to points at lower
    left (outside the gear) and upper right."""
    return diff(circle(cx, cy, r), circle(cx + d, cy + d, r))


def _to_skia(path):
    import skia
    sp = skia.Path()

    class Pen:
        def moveTo(self, p): sp.moveTo(*p)
        def lineTo(self, p): sp.lineTo(*p)
        def curveTo(self, a, b, c): sp.cubicTo(*a, *b, *c)
        def qCurveTo(self, *pts):
            if len(pts) == 2:
                sp.quadTo(*pts[0], *pts[1])
            else:  # implied on-curve points
                for k in range(len(pts) - 1):
                    a = pts[k]
                    b = pts[k + 1] if k == len(pts) - 2 else ((pts[k][0] + pts[k + 1][0]) / 2, (pts[k][1] + pts[k + 1][1]) / 2)
                    sp.quadTo(*a, *b)
        def closePath(self): sp.close()
        def endPath(self): pass
    path.draw(Pen())
    return sp


def _from_skia(sp):
    import skia
    out = Path()
    pen = out.getPen()
    it = skia.Path.Iter(sp, False)
    open_ = False
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb:
            break
        if verb == skia.Path.kMove_Verb:
            if open_:
                pen.closePath()
            pen.moveTo((pts[0].x(), pts[0].y())); open_ = True
        elif verb == skia.Path.kLine_Verb:
            pen.lineTo((pts[1].x(), pts[1].y()))
        elif verb == skia.Path.kQuad_Verb:
            pen.qCurveTo((pts[1].x(), pts[1].y()), (pts[2].x(), pts[2].y()))
        elif verb == skia.Path.kConic_Verb:
            quads = skia.Path.ConvertConicToQuads(pts[0], pts[1], pts[2], it.conicWeight(), 2)
            for k in range(1, len(quads) - 1, 2):
                pen.qCurveTo((quads[k].x(), quads[k].y()), (quads[k + 1].x(), quads[k + 1].y()))
        elif verb == skia.Path.kCubic_Verb:
            pen.curveTo((pts[1].x(), pts[1].y()), (pts[2].x(), pts[2].y()), (pts[3].x(), pts[3].y()))
        elif verb == skia.Path.kClose_Verb:
            pen.closePath(); open_ = False
    if open_:
        pen.closePath()
    return out


def halo(path, d):
    """True outward offset by d (round joins): the path plus a 2d-wide stroke."""
    import skia
    paint = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=2 * d,
                       StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap)
    stroked = skia.Path()
    paint.getFillPath(_to_skia(path), stroked)
    return union(path, _from_skia(stroked))


def emblem(with_mountain=True, with_swoosh=True, knock=5, frame="wrench", wrench_kw=None):
    """Returns dict of named layers (each a clean Path) in emblem coordinates."""
    rr = rr_mark()
    x0, y0, x1, y1 = bounds(rr)
    # with the wrench the RR is larger and breaks over the head ring: the RR stays dominant
    s = 1.34 if frame == "wrench" else 1.12
    rr = scale(move(rr, -(x0 + x1) / 2, -H), s)        # centred, baseline at y=0
    # with the mountain: baseline below centre so the peaks fill the top;
    # without it: optically centred in the wrench head
    rr = move(rr, 0, (92 if frame == "wrench" else 74) if with_mountain else H * s / 2 + 2)
    cut = halo(rr, knock)
    layers = {}
    wk = dict(WRENCH, **(wrench_kw or {}))
    g = diff(wrench(**wk) if frame == "wrench" else gear(), cut)
    if with_swoosh:
        sw = diff(swoosh(), cut)
        g = diff(g, halo(sw, knock * 0.6))
        layers["swoosh"] = sw
    if with_mountain:
        if frame == "wrench":
            # smaller peaks so the 12-point opening stays visible around them
            rock, snow = mountain(clip=circle(0, 0, 200))
            rock, snow = scale(rock, 0.9, 0, 30), scale(snow, 0.9, 0, 30)
            clip = twelve_point(wk["r_12"] - 6)
            rock, snow = inter(rock, clip), inter(snow, clip)
        else:
            rock, snow = mountain()
        rock, snow = diff(rock, cut), diff(snow, cut)
        if with_swoosh:
            sw_cut = halo(layers["swoosh"], knock * 0.6)
            rock, snow = diff(rock, sw_cut), diff(snow, sw_cut)
        layers["mountain"], layers["snow"] = rock, snow
    layers["wrench"] = g
    layers["rr"] = rr
    return layers
