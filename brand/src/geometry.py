"""Ride Rescue — monogram construction.

All marks are built on a 64-unit cap height with boolean operations
(skia-pathops), so every exported SVG is a single clean compound path:
no strokes, no overlaps, no transforms.

Requires: pip install skia-pathops fonttools
"""
import math
from pathops import Path, op, PathOp
from fontTools.pens.svgPathPen import SVGPathPen

K = 0.5522847498  # cubic Bezier circle constant

H = 64          # cap height of the monogram
T = 12          # master stroke weight (H / 5.33)
BOWL = 38       # bowl height (59% of H)


# ---------------------------------------------------------------- primitives
def rect(x0, y0, x1, y1):
    p = Path()
    p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.close()
    return p


def poly(*pts):
    p = Path()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    return p


def circle(cx, cy, r):
    k = K * r
    p = Path()
    p.moveTo(cx + r, cy)
    p.cubicTo(cx + r, cy + k, cx + k, cy + r, cx, cy + r)
    p.cubicTo(cx - k, cy + r, cx - r, cy + k, cx - r, cy)
    p.cubicTo(cx - r, cy - k, cx - k, cy - r, cx, cy - r)
    p.cubicTo(cx + k, cy - r, cx + r, cy - k, cx + r, cy)
    p.close()
    return p


def union(*paths):
    out = paths[0]
    for p in paths[1:]:
        out = op(out, p, PathOp.UNION)
    return out


def diff(a, b):
    return op(a, b, PathOp.DIFFERENCE)


def inter(a, b):
    return op(a, b, PathOp.INTERSECTION)


def capsule(x1, y1, x2, y2, w):
    """Round-capped line segment of width w (for monoline construction)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    body = poly((x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny))
    return union(body, circle(x1, y1, w / 2), circle(x2, y2, w / 2))


def leg(xa, ya, xb, yb, t=T):
    """Diagonal leg with true perpendicular thickness t, flat-cut at ya and yb."""
    dx, dy = xb - xa, yb - ya
    hw = t / 2 * math.hypot(dx, dy) / dy
    return poly((xa - hw, ya), (xa + hw, ya), (xb + hw, yb), (xb - hw, yb))


def mirror_x(path, axis=0.0):
    """Mirror a path horizontally around x = axis."""
    out = Path()
    pen = out.getPen()
    from fontTools.pens.transformPen import TransformPen
    path.draw(TransformPen(pen, (-1, 0, 0, 1, 2 * axis, 0)))
    return out


def translate(path, dx, dy=0):
    out = Path()
    from fontTools.pens.transformPen import TransformPen
    path.draw(TransformPen(out.getPen(), (1, 0, 0, 1, dx, dy)))
    return out


def scale(path, s, cx=0, cy=0):
    out = Path()
    from fontTools.pens.transformPen import TransformPen
    path.draw(TransformPen(out.getPen(), (s, 0, 0, s, cx - s * cx, cy - s * cy)))
    return out


def bounds(path):
    return path.bounds  # (xmin, ymin, xmax, ymax)


def to_d(path):
    pen = SVGPathPen(None, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    path.draw(pen)
    return pen.getCommands()


# ---------------------------------------------------------------- letter R
def bowl(x_stem, cx, t=T, h=BOWL):
    """Geometric bowl: straight bars from the stem into a true semicircle."""
    r = h / 2
    outer = union(rect(x_stem, 0, cx, h), circle(cx, r, r))
    inner = union(rect(x_stem + t, t, cx, h - t), circle(cx, r, r - t))
    # keep only the part right of the stem's left edge
    return inter(diff(outer, inner), rect(x_stem, 0, cx + r + 1, h))


def geometric_r(x0=0, leg_to=None, t=T):
    """Upright geometric R. leg_to = x of the leg's centreline at the baseline."""
    cx = x0 + 19
    stem = rect(x0, 0, x0 + t, H)
    b = bowl(x0, cx, t)
    if leg_to is None:
        leg_to = x0 + 36
    lg = leg(cx + 2, BOWL - t / 2, leg_to, H, t)
    return union(stem, b, lg)


# ---------------------------------------------------------------- concepts
def concept_a_tandem():
    """A — TANDEM. Two upright R's in sequence. The first R's leg runs
    forward until it locks into the foot of the second R's stem, closing a
    triangular counter: two letters, one connected unit."""
    gap = 8                       # vertical channel between bowl and stem
    x2 = 38 + gap                 # second R stem starts here (bowl right = 38)
    r1 = geometric_r(0, leg_to=x2 - 4)
    r2 = geometric_r(x2, leg_to=x2 + 36)
    return union(r1, r2)


def lane_mark(t=T, bowl_h=BOWL, g_top=0.75, g_bot=9.5, bowl_dx=21, leg_dx=16):
    """The Lane monogram, parameterised.

    t       stroke weight            bowl_h  bowl height
    g_top   lane half-width at the cap line (positive = the road runs out
            through the top edge and divides the two R's; negative = stems fuse)
    g_bot   lane half-width at the baseline
    bowl_dx distance from the stem's inner edge to the bowl's circle centre
    leg_dx  horizontal run of the leg from bowl junction to baseline
    """
    def gx(y):
        return g_top + (g_bot - g_top) * y / H
    stem = poly((gx(0), 0), (gx(0) + t, 0), (gx(H) + t, H), (gx(H), H))
    cx = gx(0) + bowl_dx
    r = bowl_h / 2
    outer = union(rect(gx(0), 0, cx, bowl_h), circle(cx, r, r))
    inner = union(poly((gx(t) + t, t), (cx, t), (cx, bowl_h - t), (gx(bowl_h - t) + t, bowl_h - t)),
                  circle(cx, r, r - t))
    bw = inter(diff(outer, inner), poly((gx(0), 0), (cx + r + 1, 0), (cx + r + 1, bowl_h), (gx(bowl_h), bowl_h)))
    lg = leg(cx + 2, bowl_h - t / 2, cx + 2 + leg_dx, H, t)
    right = union(stem, bw, lg)
    return union(mirror_x(right, 0), right)


# Approved master and the small-size cut for 16–31 px.
# Revision (Stage 3 review): the road now runs all the way through the cap
# line, dividing the two R's and continuing to the horizon.
LANE_MASTER = dict(g_top=0.75, g_bot=9.5)
LANE_SMALL = dict(t=10.5, bowl_h=40, g_top=0.75, g_bot=13, bowl_dx=21, leg_dx=14)
# Stage 2 concept as presented (stems fused at the top), kept so the
# exploration package still rebuilds exactly.
LANE_STAGE2 = dict(g_top=-1.2, g_bot=9)


def lane_road(g_top=LANE_MASTER["g_top"], g_bot=LANE_MASTER["g_bot"], **_):
    """The road: the negative space between the two R's, cap line to baseline."""
    if g_top <= 0:
        apex = -g_top / (g_bot - g_top) * H
        return poly((0, apex), (g_bot, H), (-g_bot, H))
    return poly((-g_top, 0), (g_top, 0), (g_bot, H), (-g_bot, H))


def concept_b_lane():
    """B — LANE (Stage 2 concept). A mirrored pair (Я|R) whose stems lean
    apart, leaving a tapered road in the negative space."""
    return lane_mark(**LANE_STAGE2)


def concept_c_route():
    """C — ROUTE. One continuous monoline path, like a route traced on a
    map: up the first stem, round the bowl, down the leg, straight into the
    second R, ending on the baseline. A solid origin dot marks the start."""
    w = 10.5                       # monoline weight
    h = w / 2
    y_top, y_base, y_bowl = h, H - h, 34
    x1 = h + 3                     # first stem centreline
    cx1 = x1 + 14                  # bowl centre x
    r = (y_bowl - y_top) / 2       # bowl centreline radius
    cy = y_top + r
    x2 = x1 + 40                   # second stem centreline
    cx2 = x2 + 14

    def r_bowl(xs, cxx):
        ring = diff(circle(cxx, cy, r + h), circle(cxx, cy, r - h))
        half = inter(ring, rect(cxx, cy - r - h - 1, cxx + r + h + 1, cy + r + h + 1))
        return union(half, capsule(xs, y_top, cxx, y_top, w), capsule(xs, y_bowl, cxx, y_bowl, w))

    parts = [
        capsule(x1, y_base, x1, y_top, w),          # stem 1
        r_bowl(x1, cx1),                           # bowl 1
        capsule(cx1 - 2, y_bowl, x2, y_base, w),    # leg 1 runs into stem 2 foot
        capsule(x2, y_base, x2, y_top, w),          # stem 2
        r_bowl(x2, cx2),                           # bowl 2
        capsule(cx2 - 2, y_bowl, x2 + 30, y_base, w),  # leg 2
        circle(x1, y_base, w * 0.78),              # origin dot
    ]
    return union(*parts)


CONCEPTS = {
    "a-tandem": ("Tandem", concept_a_tandem),
    "b-lane": ("Lane", concept_b_lane),
    "c-route": ("Route", concept_c_route),
}


def brand_r(t=T, bowl_h=BOWL, bowl_dx=21, leg_dx=16):
    """Upright R drawn with the Lane mark's bowl and leg geometry, for the
    wordmark. Returns (path at 64-unit cap height, advance-free width)."""
    stem = rect(0, 0, t, H)
    cx = bowl_dx - 1
    r = bowl_h / 2
    outer = union(rect(0, 0, cx, bowl_h), circle(cx, r, r))
    inner = union(rect(t, t, cx, bowl_h - t), circle(cx, r, r - t))
    bw = inter(diff(outer, inner), rect(0, 0, cx + r + 1, bowl_h))
    lg = leg(cx + 2, bowl_h - t / 2, cx + 2 + leg_dx, H, t)
    p = union(stem, bw, lg)
    x0, y0, x1, y1 = p.bounds
    return p, x1 - x0
