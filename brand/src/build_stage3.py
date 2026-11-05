"""Build the Stage 3 identity system (approved direction: Lane).

    python brand/src/build_stage3.py     # SVG logos, icons, graphics, tokens, board HTML
    node   brand/src/render3.js          # PNG exports, boards, PDF

Outputs go to brand/identity/.
"""
import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geometry import lane_mark, LANE_SMALL, to_d, bounds, H, T, poly, translate
from wordmark import text_path
import icons as icon_mod

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "identity")

# ------------------------------------------------------------------ colour
CORE = {
    "navy":        ("Midnight Navy",   "#14283D", (20, 40, 61),    (67, 34, 0, 76)),
    "lime":        ("Electric Lime",   "#B9E532", (185, 229, 50),  (19, 0, 78, 10)),
    "soft-white":  ("Soft White",      "#F5F6F2", (245, 246, 242), (0, 0, 2, 4)),
    "graphite":    ("Graphite",        "#252A30", (37, 42, 48),    (23, 13, 0, 81)),
    "cool-gray":   ("Cool Gray",       "#87929D", (135, 146, 157), (14, 7, 0, 38)),
    "gray-600":    ("Cool Gray 600",   "#66717D", (102, 113, 125), (18, 10, 0, 51)),
    "amber":       ("Champagne Amber", "#D99B67", (217, 155, 103), (0, 29, 53, 15)),
}
TINTS = {  # derived from core colours by mixing; UI states only
    "navy-deep":   ("#0D1A28", "Navy + 35% black: dark-mode page, footer"),
    "navy-raised": ("#24374B", "Navy + 7% white: cards and surfaces on navy"),
    "navy-line":   ("#3E4F60", "Navy + 18% white: borders and dividers on navy"),
    "navy-tint":   ("#ECEEEF", "Navy + 92% white: alternate light section"),
    "lime-hover":  ("#A5CE33", "Lime + 12% navy: primary button hover/pressed"),
    "lime-tint":   ("#F0F9D2", "Lime + 78% white: highlight background behind navy text"),
}
FUNCTIONAL = {  # not brand colours: errors only
    "alert":       ("#B42318", "Error text and borders on light (6.06:1 on Soft White)"),
    "alert-dark":  ("#FF8A7A", "Error text and borders on navy (6.55:1)"),
}
NAVY, LIME, WHITE, GRAY, GRAY600, AMBER = "#14283D", "#B9E532", "#F5F6F2", "#87929D", "#66717D", "#D99B67"

# ------------------------------------------------------------------ logo geometry
X = T                         # system unit = master stroke (12 at 64-unit mark height)
H_GAP = 2 * X                 # mark ↔ wordmark, horizontal lockup
H_CAP = H * 0.42              # wordmark cap height, horizontal lockup
S_GAP = 1.5 * X               # mark ↔ wordmark, stacked lockup
CLEAR = 2 * X                 # clear space on every side
WORD = dict(weight=800, tracking=0.06, custom_r=True)


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def svg_doc(vb, body, w=None, h=None, title=None):
    size = f' width="{w:.0f}" height="{h:.0f}"' if w else ""
    t = f"<title>{title}</title>" if title else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{size}>{t}{body}</svg>\n'


def vbox(b):
    x0, y0, x1, y1 = b
    return f"{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}"


def horizontal(mark):
    x0, y0, x1, y1 = bounds(mark)
    word, ww = text_path("RIDE RESCUE", H_CAP, **WORD)
    ox, oy = x1 + H_GAP, (H - H_CAP) / 2
    return word, (ox, oy), (x0, 0, ox + ww, H)


def stacked(mark):
    x0, y0, x1, y1 = bounds(mark)
    mw = x1 - x0
    # wordmark sized to twice the mark's width
    probe, pw = text_path("RIDE RESCUE", 10, **WORD)
    cap = 10 * (2 * mw) / pw
    word, ww = text_path("RIDE RESCUE", cap, **WORD)
    ox, oy = -ww / 2, H + S_GAP
    return word, (ox, oy), (-ww / 2, 0, ww / 2, H + S_GAP + cap), cap


def lockup_svg(mark, word, off, b, mark_fill, word_fill, bg=None, pad=0):
    x0, y0, x1, y1 = b
    vb = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    body = ""
    if bg:
        body += f'<rect x="{vb[0]:.2f}" y="{vb[1]:.2f}" width="{vb[2] - vb[0]:.2f}" height="{vb[3] - vb[1]:.2f}" fill="{bg}"/>'
    body += f'<path fill="{mark_fill}" d="{to_d(mark)}"/>'
    body += f'<path fill="{word_fill}" transform="translate({off[0]:.2f} {off[1]:.2f})" d="{to_d(word)}"/>'
    return svg_doc(vbox(vb), body, title="Ride Rescue")


COLORWAYS = {
    # name: (mark, wordmark, intended background)
    "navy":  (NAVY, NAVY, "light backgrounds: Soft White, white, light photos. Also the monochrome navy version"),
    "dark":  (LIME, WHITE, "navy, graphite and dark photos (primary full-colour version)"),
    "black": ("#000000", "#000000", "one-colour black: fax, engraving, newspaper, single-colour print"),
    "white": ("#FFFFFF", "#FFFFFF", "one-colour white: reversed out of any dark colour or photo"),
    "lime":  (LIME, LIME, "monochrome lime: navy or graphite backgrounds only, never on light"),
}


def build_logos(manifest):
    master = lane_mark()
    small = lane_mark(**LANE_SMALL)
    files = []

    for cw, (mf, wf, use) in COLORWAYS.items():
        word, off, b = horizontal(master)
        name = f"logo/svg/ride-rescue-horizontal-{cw}.svg"
        write(name, lockup_svg(master, word, off, b, mf, wf))
        files.append((name, "Horizontal lockup", use))

        word, off, b, _ = stacked(master)
        name = f"logo/svg/ride-rescue-stacked-{cw}.svg"
        write(name, lockup_svg(master, word, off, b, mf, wf))
        files.append((name, "Stacked lockup", use))

    for cw, fill in (("navy", NAVY), ("lime", LIME), ("white", "#FFFFFF"), ("black", "#000000")):
        name = f"logo/svg/rr-monogram-{cw}.svg"
        write(name, svg_doc(vbox(bounds(master)), f'<path fill="{fill}" d="{to_d(master)}"/>', title="Ride Rescue RR monogram"))
        files.append((name, "RR monogram (master, 32 px and up)", cw))
        name = f"logo/svg/rr-monogram-small-{cw}.svg"
        write(name, svg_doc(vbox(bounds(small)), f'<path fill="{fill}" d="{to_d(small)}"/>', title="Ride Rescue RR monogram, small-size cut"))
        files.append((name, "RR monogram small-size cut (16-31 px)", cw))

    for cw, fill in (("navy", NAVY), ("white", WHITE), ("black", "#000000"), ("lime", LIME)):
        word, ww = text_path("RIDE RESCUE", H_CAP, **WORD)
        name = f"logo/svg/ride-rescue-wordmark-{cw}.svg"
        write(name, svg_doc(f"0 0 {ww:.2f} {H_CAP:.2f}", f'<path fill="{fill}" d="{to_d(word)}"/>', title="Ride Rescue"))
        files.append((name, "Wordmark", cw))

    manifest["logos"] = [{"file": f, "type": t, "use": u} for f, t, u in files]

    # construction + clear-space diagrams
    word, off, b = horizontal(master)
    x0, y0, x1, y1 = b
    c = CLEAR
    mx1 = bounds(master)[2]
    sq = lambda x, y: f'<rect x="{x:.2f}" y="{y:.2f}" width="{X}" height="{X}" fill="{LIME}" fill-opacity=".6" stroke="{NAVY}" stroke-width=".4"/>'
    guides = (f'<rect x="{x0 - c}" y="{y0 - c}" width="{x1 - x0 + 2 * c}" height="{y1 - y0 + 2 * c}" fill="none" stroke="{AMBER}" stroke-width="0.8" stroke-dasharray="3 2"/>'
              f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{GRAY}" stroke-width="0.5"/>')
    xs = sq(x0 - 2 * X, H / 2 - X / 2) + sq(x0 - X, H / 2 - X / 2)
    xs += sq(x1 - X * 5, y0 - 2 * X) + sq(x1 - X * 5, y0 - X)
    xs += sq(mx1, H / 2 - X / 2) + sq(mx1 + X, H / 2 - X / 2)
    xs += sq(x1 + X, H / 2 - X / 2) + sq(x1, H / 2 - X / 2)
    font = 'font-family="Helvetica, Arial, sans-serif" font-weight="700"'
    lbl = (f'<text x="{x0 - c}" y="{y0 - c - 6}" {font} font-size="9" fill="{GRAY600}">Clear space 2X on every side · mark to wordmark gap 2X</text>'
           f'<text x="{x0 - c}" y="{y1 + c + 13}" {font} font-size="9" fill="{GRAY600}">X = monogram stroke = mark height / 5.33</text>')
    body = (f'<path fill="{NAVY}" d="{to_d(master)}"/><path fill="{NAVY}" transform="translate({off[0]} {off[1]})" d="{to_d(word)}"/>'
            + guides + xs + lbl)
    write("logo/diagrams/clear-space-horizontal.svg",
          svg_doc(f"{x0 - c - 6} {y0 - c - 20} {x1 - x0 + 2 * c + 12} {y1 - y0 + 2 * c + 40}", body))

    # monogram construction
    mx0, my0, mx1, my1 = bounds(master)
    apex = 1.2 / (9 + 1.2) * H
    lines = "".join(f'<line x1="{mx0 - 6}" x2="{mx1 + 6}" y1="{y}" y2="{y}" stroke="{AMBER}" stroke-width=".35" stroke-dasharray="1.5 1"/>' for y in (0, T, 38 - T, 38, H))
    lines += f'<line x1="0" x2="0" y1="-4" y2="{H + 4}" stroke="{AMBER}" stroke-width=".35"/>'
    body = (f'<path fill="{NAVY}" fill-opacity=".1" stroke="{NAVY}" stroke-width=".45" d="{to_d(master)}"/>'
            f'<path fill="{LIME}" d="{to_d(poly((0, apex), (9, H), (-9, H)))}"/>' + lines
            + "".join(f'<text x="{mx1 + 8}" y="{y + 1.5}" font-family="Helvetica, Arial, sans-serif" font-weight="700" font-size="3.2" fill="{GRAY600}">{t}</text>'
                      for y, t in ((0, "cap line · 64"), (T, "stroke 12"), (38, "bowl 38"), (H, "baseline"))))
    write("logo/diagrams/monogram-construction.svg", svg_doc(f"{mx0 - 8} -6 {mx1 - mx0 + 44} {H + 12}", body))


# ------------------------------------------------------------------ icons
def build_icons(manifest):
    names = []
    sprite = ""
    for key, (label, body) in icon_mod.ICONS.items():
        write(f"icons/svg/{key}.svg", icon_mod.svg(key))
        sprite += f'<symbol id="rr-{key}" viewBox="0 0 24 24"><title>{escape(label)}</title>{body}</symbol>'
        names.append({"id": key, "label": label})
    write("icons/sprite.svg",
          '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" fill="none" stroke="currentColor" '
          f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{sprite}</svg>\n')
    manifest["icons"] = names


# ------------------------------------------------------------------ graphic language
def build_graphics():
    apex = 1.2 / (9 + 1.2) * H
    wedge = poly((0, apex), (9, H), (-9, H))
    for cw, fill in (("lime", LIME), ("raised", "#24374B"), ("navy", NAVY)):
        write(f"graphics/lane-wedge-{cw}.svg", svg_doc(f"-9 {apex:.2f} 18 {H - apex:.2f}", f'<path fill="{fill}" d="{to_d(wedge)}"/>'))
    # tapered divider: the lane laid on its side
    for cw, fill in (("navy", NAVY), ("lime", LIME)):
        write(f"graphics/lane-divider-{cw}.svg", svg_doc("0 0 240 6", f'<path fill="{fill}" d="M0 0L240 3L0 6Z"/>'))
    # road-marking pattern tile: staggered dashes on the 12-unit rhythm
    tile = ('<rect width="48" height="24" fill="#14283D"/>'
            '<g fill="#24374B"><rect x="0" y="5" width="16" height="2" rx="1"/><rect x="24" y="5" width="16" height="2" rx="1"/>'
            '<rect x="12" y="17" width="16" height="2" rx="1"/><rect x="36" y="17" width="12" height="2" rx="1"/><rect x="0" y="17" width="4" height="2" rx="1"/></g>')
    write("graphics/pattern-road-tile.svg", svg_doc("0 0 48 24", tile, 48, 24))
    # directional wedge (points right) for "next" cues
    for cw, fill in (("navy", NAVY), ("lime", LIME)):
        write(f"graphics/direction-wedge-{cw}.svg", svg_doc("0 0 56 18", f'<path fill="{fill}" d="M0 0L56 9L0 18Z"/>'))
    # cut-corner frame: rectangle with the top-right corner clipped at 45 degrees
    write("graphics/cut-corner-frame.svg", svg_doc("0 0 320 200", '<path fill="#14283D" d="M0 0H284L320 36V200H0Z"/>'))


# ------------------------------------------------------------------ tokens
def build_tokens():
    tokens = {
        "color": {
            "brand": {k: {"name": v[0], "hex": v[1], "rgb": v[2], "cmyk": v[3]} for k, v in CORE.items()},
            "tint": {k: {"hex": v[0], "use": v[1]} for k, v in TINTS.items()},
            "functional": {k: {"hex": v[0], "use": v[1]} for k, v in FUNCTIONAL.items()},
        },
        "font": {
            "brand": "Manrope, system-ui, sans-serif",
            "ui": "Inter, system-ui, sans-serif",
        },
        "radius": {"sm": "6px", "md": "10px", "lg": "16px", "pill": "999px"},
        "space-unit": "4px",
    }
    write("tokens/tokens.json", json.dumps(tokens, indent=2))

    css = ["/* Ride Rescue design tokens — generated by brand/src/build_stage3.py */", ":root {"]
    for k, v in CORE.items():
        css.append(f"  --rr-{k}: {v[1]};")
    for k, v in TINTS.items():
        css.append(f"  --rr-{k}: {v[0]};")
    for k, v in FUNCTIONAL.items():
        css.append(f"  --rr-{k}: {v[0]};")
    css += [
        "",
        "  /* semantic: light theme */",
        "  --rr-bg: var(--rr-soft-white);",
        "  --rr-bg-alt: var(--rr-navy-tint);",
        "  --rr-surface: #ffffff;",
        "  --rr-text: var(--rr-navy);",
        "  --rr-text-muted: var(--rr-gray-600);",
        "  --rr-border: #D5DADF;",
        "  --rr-accent-ink: var(--rr-navy);       /* lines, ticks, links on light */",
        "  --rr-action-bg: var(--rr-lime);",
        "  --rr-action-bg-hover: var(--rr-lime-hover);",
        "  --rr-action-text: var(--rr-navy);",
        "  --rr-focus: var(--rr-navy);",
        "  --rr-error: var(--rr-alert);",
        "",
        "  --rr-font-brand: Manrope, system-ui, sans-serif;",
        "  --rr-font-ui: Inter, system-ui, sans-serif;",
        "  --rr-radius-sm: 6px; --rr-radius-md: 10px; --rr-radius-lg: 16px;",
        "}",
        "",
        "/* semantic: dark theme (also used for always-dark sections such as the hero) */",
        "[data-theme=\"dark\"], .rr-dark {",
        "  --rr-bg: var(--rr-navy-deep);",
        "  --rr-bg-alt: var(--rr-navy);",
        "  --rr-surface: var(--rr-navy-raised);",
        "  --rr-text: var(--rr-soft-white);",
        "  --rr-text-muted: var(--rr-cool-gray);",
        "  --rr-border: var(--rr-navy-line);",
        "  --rr-accent-ink: var(--rr-lime);",
        "  --rr-focus: var(--rr-lime);",
        "  --rr-error: var(--rr-alert-dark);",
        "}",
    ]
    write("tokens/tokens.css", "\n".join(css) + "\n")


def main():
    manifest = {}
    build_logos(manifest)
    build_icons(manifest)
    build_graphics()
    build_tokens()
    write("manifest.json", json.dumps(manifest, indent=2))
    print("identity written to", OUT)


if __name__ == "__main__":
    main()
