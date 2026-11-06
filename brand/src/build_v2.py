"""Ride Rescue identity v2 — build every logo, token and graphic.

    python brand/src/build_v2.py      # SVG masters, promo SVG, tokens, graphics, icons
    python brand/src/boards_v2.py     # presentation boards (HTML)
    node   brand/src/render_v2.js     # PNG exports, size tests, boards, PDF

Outputs: brand/identity/
"""
import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import to_d, bounds, union, poly
from rr2 import (rr_mark, emblem, italic, r_upright, scale, move, H, X, W)
from wordmark import set_text
import icons as icon_mod

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "identity")
FONTS = os.path.join(ROOT, "fonts")
SAIRA_I = os.path.join(FONTS, "Saira-Italic-Variable.ttf")

# ------------------------------------------------------------------ colour
CORE = {
    "electric-blue": ("Electric Blue", "#087FFF", (8, 127, 255), (97, 50, 0, 0)),
    "steel-silver":  ("Steel Silver",  "#C3C9D0", (195, 201, 208), (6, 3, 0, 18)),
    "carbon-black":  ("Carbon Black",  "#111315", (17, 19, 21), (19, 10, 0, 92)),
    "white":         ("White",         "#FFFFFF", (255, 255, 255), (0, 0, 0, 0)),
}
DERIVED = {  # proposed refinements, each mixed from the core four
    "action-blue": ("#0973E5", "Blue + 11% carbon. Buttons and links: white label 4.57:1, on white 4.57:1"),
    "steel-600":   ("#73777C", "Silver + 45% carbon. Wrench on light backgrounds, muted text on white (4.51:1)"),
    "carbon-raised": ("#1F2123", "Carbon + 6% white. Cards and surfaces on dark"),
    "carbon-line": ("#37393A", "Carbon + 16% white. Borders and dividers on dark"),
    "steel-tint":  ("#F0F2F3", "Silver + 75% white. Alternate light section"),
    "blue-tint":   ("#E6F2FF", "Blue + 90% white. Selected/highlight background behind carbon text"),
}
FUNCTIONAL = {"alert": ("#C4320A", "Errors on light"), "alert-dark": ("#FF8A66", "Errors on dark")}

BLUE, SILVER, CARBON, WHITE = "#087FFF", "#C3C9D0", "#111315", "#FFFFFF"
STEEL600 = "#73777C"

# colourways: layer -> colour
WAYS = {
    "dark":  dict(rr=WHITE, wrench=SILVER, mountain=SILVER, snow=WHITE, swoosh=BLUE, ride=SILVER, rescue=BLUE, tag=WHITE, rule=BLUE),
    "light": dict(rr=CARBON, wrench=STEEL600, mountain=STEEL600, snow=SILVER, swoosh=BLUE, ride=CARBON, rescue=BLUE, tag=CARBON, rule=BLUE),
    "black": {k: "#000000" for k in ("rr", "wrench", "mountain", "snow", "swoosh", "ride", "rescue", "tag", "rule")},
    "white": {k: WHITE for k in ("rr", "wrench", "mountain", "snow", "swoosh", "ride", "rescue", "tag", "rule")},
}
WAY_USE = {
    "dark": "Full colour on Carbon Black or dark photography (primary)",
    "light": "Full colour on white and light backgrounds",
    "black": "One colour: single-colour print, engraving, fax, stamps",
    "white": "One colour reversed: vinyl on dark vehicles, embroidery on dark garments, dark photos",
}

# ------------------------------------------------------------------ type
WORD_AXES = {"wdth": 112, "wght": 800}
TAG_AXES = {"wdth": 100, "wght": 600}
TAGLINE = "MOBILE DIAGNOSTICS • PROGRAMMING • REPAIRS"


def custom_r(cap):
    """Monogram R, slanted, scaled to the wordmark's cap height."""
    r = italic(r_upright())
    x0, _, x1, _ = bounds(r)
    k = cap / H
    lsb = 0.015 * cap
    return move(scale(move(r, -x0), k), lsb), (x1 - x0) * k + 0.045 * cap


def wordmark(cap):
    """Returns (ride_path, rescue_path, total_width) with RESCUE positioned."""
    ride, wr = set_text("RIDE", cap, SAIRA_I, WORD_AXES, 0.02, glyph_override={"R": custom_r})
    space = 0.32 * cap
    rescue, ws = set_text("RESCUE", cap, SAIRA_I, WORD_AXES, 0.02, glyph_override={"R": custom_r})
    return ride, move(rescue, wr + space), wr + space + ws


def tagline(cap):
    return set_text(TAGLINE, cap, SAIRA_I, TAG_AXES, 0.16)


def road_rule(width, thick):
    """Tapered road line (both ends): the RR's road line used as a rule."""
    return poly((0, thick / 2), (width / 2, 0), (width, thick / 2), (width / 2, thick))


# ------------------------------------------------------------------ svg helpers
def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def doc(b, body, pad=0, title="Ride Rescue"):
    x0, y0, x1, y1 = b
    vb = f"{x0 - pad:.2f} {y0 - pad:.2f} {x1 - x0 + 2 * pad:.2f} {y1 - y0 + 2 * pad:.2f}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><title>{escape(title)}</title>{body}</svg>\n'


def layer(path, fill, tf=None):
    t = f' transform="{tf}"' if tf else ""
    return f'<path fill="{fill}"{t} d="{to_d(path)}"/>'


def ub(*paths):
    return bounds(union(*paths))


# ------------------------------------------------------------------ compositions
def emblem_layers(full=True):
    return emblem(with_mountain=full, with_swoosh=full)


def stacked(full_emblem=True):
    L = emblem_layers(full_emblem)
    ex0, ey0, ex1, ey1 = ub(*L.values())
    ew = ex1 - ex0
    cap = ew * 0.215
    ride, rescue, ww = wordmark(cap)
    tag, tw = tagline(cap * 0.24)
    gap = ew * 0.07
    y_word = ey1 + gap
    x_word = (ex0 + ex1) / 2 - ww / 2
    rule_w = ww * 1.04
    rule = move(road_rule(rule_w, cap * 0.07), (ex0 + ex1) / 2 - rule_w / 2, y_word + cap + gap * 0.45)
    y_tag = y_word + cap + gap * 0.45 + cap * 0.07 + gap * 0.45
    tag = move(tag, (ex0 + ex1) / 2 - tw / 2, y_tag)
    parts = dict(L)
    parts.update(ride=move(ride, x_word, y_word), rescue=move(rescue, x_word, y_word), rule=rule, tag=tag)
    return parts


def horizontal(full_emblem=True):
    L = emblem_layers(full_emblem)
    ex0, ey0, ex1, ey1 = ub(*L.values())
    eh = ey1 - ey0
    cap = eh * 0.25
    ride, rescue, ww = wordmark(cap)
    tag, tw = tagline(cap * 0.255)
    # stretch the tagline's tracking? keep natural, align left under the wordmark
    gap = eh * 0.10
    x_text = ex1 + gap
    block = cap + cap * 0.32 + cap * 0.07 + cap * 0.32 + cap * 0.255
    y_word = (ey0 + ey1) / 2 - block / 2
    rule = move(road_rule(ww, cap * 0.07), x_text, y_word + cap + cap * 0.32)
    tag = move(tag, x_text, y_word + cap + cap * 0.32 + cap * 0.07 + cap * 0.32)
    parts = dict(L)
    parts.update(ride=move(ride, x_text, y_word), rescue=move(rescue, x_text, y_word), rule=rule, tag=tag)
    return parts


def render_parts(parts, way):
    c = WAYS[way]
    order = ["wrench", "mountain", "snow", "swoosh", "rr", "ride", "rescue", "rule", "tag"]
    return "".join(layer(parts[k], c[k]) for k in order if k in parts)


# ------------------------------------------------------------------ promotional chrome
PROMO_DEFS = """
<defs>
 <linearGradient id="towH" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0e10"/><stop offset=".5" stop-color="#2b2f34"/><stop offset="1" stop-color="#0d0e10"/></linearGradient>
 <linearGradient id="towV" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0b0c0d"/><stop offset=".5" stop-color="#1f2226"/><stop offset="1" stop-color="#0b0c0d"/></linearGradient>
 <pattern id="carbon" width="16" height="16" patternUnits="userSpaceOnUse">
  <rect width="8" height="8" fill="url(#towH)"/><rect x="8" y="8" width="8" height="8" fill="url(#towH)"/>
  <rect x="8" width="8" height="8" fill="url(#towV)"/><rect y="8" width="8" height="8" fill="url(#towV)"/>
 </pattern>
 <radialGradient id="vignette" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".6" stop-color="#000" stop-opacity=".25"/><stop offset="1" stop-color="#000" stop-opacity=".8"/></radialGradient>
 <radialGradient id="bg" cx="50%" cy="38%" r="75%">
  <stop offset="0" stop-color="#2a2e33"/><stop offset=".55" stop-color="#16181b"/><stop offset="1" stop-color="#0a0b0c"/>
 </radialGradient>
 <linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".28" stop-color="#d9dee3"/><stop offset=".48" stop-color="#8d96a0"/>
  <stop offset=".52" stop-color="#5d6670"/><stop offset=".7" stop-color="#c3c9d0"/><stop offset="1" stop-color="#f4f6f8"/>
 </linearGradient>
 <linearGradient id="steel" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#eef1f4"/><stop offset=".45" stop-color="#aab2bb"/><stop offset=".55" stop-color="#7c858f"/><stop offset="1" stop-color="#d3d8de"/>
 </linearGradient>
 <linearGradient id="blue" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#7cc0ff"/><stop offset=".45" stop-color="#087FFF"/><stop offset="1" stop-color="#0352ad"/>
 </linearGradient>
 <filter id="bevel" x="-10%" y="-10%" width="120%" height="120%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="1.4" result="b"/>
  <feSpecularLighting in="b" surfaceScale="3" specularConstant=".9" specularExponent="22" lighting-color="#ffffff" result="s">
   <fePointLight x="-200" y="-400" z="300"/></feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".55" k4="0"/>
 </filter>
 <filter id="lift" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#000" flood-opacity=".75"/>
 </filter>
 <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur stdDeviation="6" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
</defs>"""


def promo_svg(parts, b, pad):
    x0, y0, x1, y1 = b
    fills = dict(wrench="url(#steel)", mountain="url(#steel)", snow="#ffffff", swoosh="url(#blue)",
                 rr="url(#chrome)", ride="url(#chrome)", rescue="url(#blue)", rule="url(#blue)", tag="#ffffff")
    body = PROMO_DEFS
    rx, ry, rw, rh = x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad
    body += f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="url(#carbon)"/>'
    body += f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="url(#vignette)"/>'
    body += '<g filter="url(#lift)">'
    for k in ["wrench", "mountain", "snow"]:
        if k in parts:
            body += f'<path fill="{fills[k]}" filter="url(#bevel)" d="{to_d(parts[k])}"/>'
    if "swoosh" in parts:
        body += f'<path fill="{fills["swoosh"]}" filter="url(#glow)" d="{to_d(parts["swoosh"])}"/>'
    for k in ["rr", "ride", "rescue", "rule", "tag"]:
        if k in parts:
            f = ' filter="url(#bevel)"' if k in ("rr", "ride", "rescue") else ""
            body += f'<path fill="{fills[k]}"{f} d="{to_d(parts[k])}"/>'
    body += "</g>"
    return doc(b, body, pad, "Ride Rescue promotional logo (derived from flat master)")


# ------------------------------------------------------------------ build
def build_logos(manifest):
    entries = []

    mark = rr_mark()
    for way, col in (("white", WHITE), ("carbon", CARBON), ("blue", BLUE), ("silver", SILVER), ("black", "#000000")):
        n = f"logo/svg/rr-micro-{way}.svg"
        write(n, doc(bounds(mark), layer(mark, col), title="Ride Rescue RR monogram"))
        entries.append((n, "Micro mark (RR)", way))

    for full, name, label in ((False, "rr-wrench", "Secondary: RR in wrench"), (True, "emblem", "Primary emblem")):
        L = emblem_layers(full)
        for way in WAYS:
            n = f"logo/svg/{name}-{way}.svg"
            write(n, doc(ub(*L.values()), render_parts(L, way)))
            entries.append((n, label, WAY_USE[way]))

    for fn, name, label in ((stacked, "ride-rescue-stacked", "Primary lockup, stacked"),
                            (horizontal, "ride-rescue-horizontal", "Primary lockup, horizontal")):
        P = fn(True)
        for way in WAYS:
            n = f"logo/svg/{name}-{way}.svg"
            write(n, doc(ub(*P.values()), render_parts(P, way)))
            entries.append((n, label, WAY_USE[way]))
        n = f"logo/promo/{name}-chrome.svg"
        write(n, promo_svg(P, ub(*P.values()), 40))
        entries.append((n, label + ", promotional chrome", "Banners, ads, presentations, video. Never as the master"))

    # secondary horizontal: RR-in-wrench + wordmark (no mountain), for headers
    P = horizontal(False)
    for way in WAYS:
        n = f"logo/svg/ride-rescue-horizontal-compact-{way}.svg"
        write(n, doc(ub(*P.values()), render_parts(P, way)))
        entries.append((n, "Compact horizontal (wrench, no mountain)", WAY_USE[way]))

    # wordmark alone, and wordmark + tagline
    cap = 64
    ride, rescue, ww = wordmark(cap)
    tag, tw = tagline(cap * 0.255)
    rule = move(road_rule(ww, cap * 0.07), 0, cap + cap * 0.32)
    tag = move(tag, 0, cap + cap * 0.32 + cap * 0.07 + cap * 0.32)
    for way in WAYS:
        c = WAYS[way]
        n = f"logo/svg/ride-rescue-wordmark-{way}.svg"
        write(n, doc(ub(ride, rescue), layer(ride, c["ride"]) + layer(rescue, c["rescue"])))
        entries.append((n, "Wordmark", WAY_USE[way]))
        n = f"logo/svg/ride-rescue-wordmark-tagline-{way}.svg"
        write(n, doc(ub(ride, rescue, rule, tag), layer(ride, c["ride"]) + layer(rescue, c["rescue"]) + layer(rule, c["rule"]) + layer(tag, c["tag"])))
        entries.append((n, "Wordmark with tagline", WAY_USE[way]))

    # promo emblem alone (square, for social/video)
    L = emblem_layers(True)
    write("logo/promo/emblem-chrome.svg", promo_svg(L, ub(*L.values()), 30))
    entries.append(("logo/promo/emblem-chrome.svg", "Emblem, promotional chrome", "Social, video, merchandise mockups"))

    manifest["logos"] = [{"file": f, "type": t, "use": u} for f, t, u in entries]


def build_diagrams():
    # micro mark construction (upright parts before the 12-degree slant)
    from rr2 import r_upright as ru
    up = ru()
    guides = "".join(f'<line x1="-6" x2="{W + 14}" y1="{y}" y2="{y}" stroke="#D99B67" stroke-width=".35" stroke-dasharray="1.5 1"/>'
                     for y in (0, X, 46 - X, 46, H))
    lbl = "".join(f'<text x="{W + 16}" y="{y + 1.4}" font-family="Helvetica, Arial, sans-serif" font-size="3.2" font-weight="700" fill="#73777C">{t}</text>'
                  for y, t in ((0, "cap 64"), (X, "stroke 16 = X"), (46, "bowl 46"), (H, "baseline")))
    up_svg = f'<path fill="#111315" fill-opacity=".12" stroke="#111315" stroke-width=".45" d="{to_d(up)}"/>' + guides + lbl
    write("logo/diagrams/r-construction-upright.svg", doc((-8, -6, W + 40, H + 6), up_svg))
    m = rr_mark()
    x0, y0, x1, y1 = bounds(m)
    sl = (f'<path fill="#111315" d="{to_d(m)}"/>'
          f'<line x1="{x0}" y1="{H}" x2="{x0 + 0.2126 * H}" y2="0" stroke="#087FFF" stroke-width=".6"/>'
          f'<text x="{x0 + 3}" y="{H + 6}" font-family="Helvetica, Arial, sans-serif" font-size="4" font-weight="700" fill="#73777C">12° slant · road line runs on past the second R</text>')
    write("logo/diagrams/rr-construction.svg", doc((x0 - 4, -4, x1 + 4, H + 9), sl))


def build_tokens():
    tokens = {
        "color": {
            "brand": {k: {"name": v[0], "hex": v[1], "rgb": v[2], "cmyk": v[3]} for k, v in CORE.items()},
            "derived": {k: {"hex": v[0], "use": v[1]} for k, v in DERIVED.items()},
            "functional": {k: {"hex": v[0], "use": v[1]} for k, v in FUNCTIONAL.items()},
        },
        "font": {"display": "Saira (italic, wdth 112, wght 800)", "ui": "Inter"},
    }
    write("tokens/tokens.json", json.dumps(tokens, indent=2))
    css = ["/* Ride Rescue design tokens, identity v2 (generated by brand/src/build_v2.py) */", ":root {"]
    css += [f"  --rr-{k}: {v[1]};" for k, v in CORE.items()]
    css += [f"  --rr-{k}: {v[0]};" for k, v in DERIVED.items()]
    css += [f"  --rr-{k}: {v[0]};" for k, v in FUNCTIONAL.items()]
    css += ["",
            "  --rr-font-display: \"Saira\", system-ui, sans-serif;   /* use font-style: italic; font-stretch: 112%; */",
            "  --rr-font-ui: \"Inter\", system-ui, sans-serif;",
            "  /* semantic, light */",
            "  --rr-bg: var(--rr-white); --rr-bg-alt: var(--rr-steel-tint); --rr-text: var(--rr-carbon-black);",
            "  --rr-text-muted: var(--rr-steel-600); --rr-border: #D7DBDF; --rr-link: var(--rr-action-blue);",
            "  --rr-action-bg: var(--rr-action-blue); --rr-action-text: var(--rr-white);",
            "}",
            "[data-theme=\"dark\"], .rr-dark {",
            "  --rr-bg: var(--rr-carbon-black); --rr-bg-alt: var(--rr-carbon-raised); --rr-text: var(--rr-white);",
            "  --rr-text-muted: var(--rr-steel-silver); --rr-border: var(--rr-carbon-line); --rr-link: var(--rr-electric-blue);",
            "  --rr-action-bg: var(--rr-electric-blue); --rr-action-text: var(--rr-carbon-black);",
            "}"]
    write("tokens/tokens.css", "\n".join(css) + "\n")


def build_icons(manifest):
    sprite = ""
    for key, (label, body) in icon_mod.ICONS.items():
        write(f"icons/svg/{key}.svg", icon_mod.svg(key))
        sprite += f'<symbol id="rr-{key}" viewBox="0 0 24 24"><title>{escape(label)}</title>{body}</symbol>'
    write("icons/sprite.svg", '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" fill="none" stroke="currentColor" '
          f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{sprite}</svg>\n')
    manifest["icons"] = [{"id": k, "label": v[0]} for k, v in icon_mod.ICONS.items()]


def intersect_box(path, x0, y0, x1, y1):
    from geometry import inter, rect
    return inter(path, rect(x0, y0, x1, y1))


def build_graphics():
    from rr2 import swoosh, mountain
    # road line (tapered both ends)
    for c, col in (("blue", BLUE), ("carbon", CARBON), ("silver", SILVER)):
        write(f"graphics/road-line-{c}.svg", doc((0, 0, 480, 8), layer(road_rule(480, 8), col)))
    # swoosh arc
    sw = swoosh()
    write("graphics/swoosh-blue.svg", doc(bounds(sw), layer(sw, BLUE)))
    # ridge line: the mountain silhouette as a horizon band
    rock, snow = mountain(r_clip=200)
    ridge = union(rock, snow)
    # horizon band: the ridge widened and run out to both edges
    from rr2 import xform
    band = union(xform(ridge, 2.4, 0, 0, 0.7, 0, 0), poly((-400, 20), (-148, 8.4), (148, 2.8), (400, 14), (400, 28), (-400, 28)))
    band = intersect_box(band, -400, -60, 400, 28)
    write("graphics/ridge-band-raised.svg", doc(bounds(band), layer(band, "#1F2123")))
    write("graphics/ridge-band-silver.svg", doc(bounds(band), layer(band, SILVER)))
    write("graphics/ridge-silver.svg", doc(bounds(ridge), layer(ridge, SILVER)))
    write("graphics/ridge-carbon-raised.svg", doc(bounds(ridge), layer(ridge, "#1F2123")))
    # 12-point ratchet ring: corners and section heads
    from rr2 import twelve_point, wrench, WRENCH
    from geometry import circle as _circle, diff as _diff
    ring = _diff(_circle(0, 0, 84), twelve_point(72))
    write("graphics/ratchet-ring-silver.svg", doc(bounds(ring), layer(ring, SILVER)))
    write("graphics/ratchet-ring-raised.svg", doc(bounds(ring), layer(ring, "#1F2123")))
    w = wrench(**WRENCH)
    write("graphics/wrench-only.svg", doc(bounds(w), layer(w, STEEL600)))  # misuse board only
    # carbon-fibre plain weave tile (textures and promotional backgrounds only)
    tile = (PROMO_DEFS.split("<pattern")[0] + '</defs>'
            '<rect width="8" height="8" fill="url(#towH)"/><rect x="8" y="8" width="8" height="8" fill="url(#towH)"/>'
            '<rect x="8" width="8" height="8" fill="url(#towV)"/><rect y="8" width="8" height="8" fill="url(#towV)"/>')
    write("graphics/carbon-fibre-tile.svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">{tile}</svg>\n')


def main():
    manifest = {}
    build_logos(manifest)
    build_diagrams()
    build_tokens()
    build_icons(manifest)
    build_graphics()
    write("manifest.json", json.dumps(manifest, indent=2))
    print("identity v2 written to", OUT, "-", len(manifest["logos"]), "logo files")


if __name__ == "__main__":
    main()
