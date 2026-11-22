"""Stage 3 presentation boards (HTML → PNG/PDF via render3.js)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons as icon_mod
from build_stage3 import CORE, TINTS, FUNCTIONAL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "archive", "lane-v1", "identity", "boards")
L = "../logo/svg/"
NAVY, LIME, WHITE, GRAY, GRAY600, AMBER = "#14283D", "#B9E532", "#F5F6F2", "#87929D", "#66717D", "#D99B67"

CSS = f"""
@font-face{{font-family:Manrope;src:url(../../../../fonts/Manrope-Variable.ttf);font-weight:200 800}}
@font-face{{font-family:Inter;src:url(../../../../fonts/Inter-Variable.ttf);font-weight:100 900}}
*{{box-sizing:border-box}}
body{{margin:0;background:{WHITE};color:{NAVY};font-family:Inter,sans-serif;width:1200px}}
.board{{padding:48px}}
.kicker{{font:800 13px Manrope;letter-spacing:.14em;text-transform:uppercase;color:{GRAY600};margin:0 0 6px}}
h1{{font:800 40px/1.1 Manrope;margin:0 0 10px;letter-spacing:-.01em}}
h2{{font:800 18px Manrope;margin:0 0 12px}}
.lead{{font-size:17px;line-height:1.55;max-width:900px;margin:0 0 28px;color:#2b3a4a}}
.g{{display:grid;gap:16px;margin-bottom:16px}}
.g2{{grid-template-columns:1fr 1fr}} .g3{{grid-template-columns:repeat(3,1fr)}} .g4{{grid-template-columns:repeat(4,1fr)}}
.p{{border-radius:16px;padding:28px;position:relative;display:flex;align-items:center;justify-content:center;min-height:180px}}
.lt{{background:#fff;border:1px solid #dfe3e6}} .dk{{background:{NAVY};color:{WHITE}}} .gr{{background:#252A30;color:{WHITE}}}
.lab{{position:absolute;left:14px;top:10px;font:700 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:{GRAY600}}}
.dk .lab,.gr .lab{{color:#9fb0c1}}
.n{{display:inline-block;background:{LIME};color:{NAVY};font:800 11px Inter;border-radius:999px;padding:2px 8px;margin-right:6px}}
.note{{font-size:14px;line-height:1.55;color:#2b3a4a}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{padding:7px 8px;border-bottom:1px solid #e3e6e8;text-align:left;vertical-align:top}}
th{{font:700 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:{GRAY600}}}
.sw{{border-radius:14px;overflow:hidden;border:1px solid #dfe3e6;background:#fff}}
.sw .c{{height:120px;display:flex;align-items:flex-end;padding:12px;font:800 15px Manrope}}
.sw .m{{padding:12px;font-size:12.5px;line-height:1.6;font-family:Inter;font-feature-settings:"tnum"}}
.btn{{display:inline-flex;align-items:center;justify-content:center;padding:12px 20px;border-radius:10px;font:700 15px Inter;margin:4px}}
.dont{{flex-direction:column;gap:12px}} .dont img{{max-height:56px;max-width:85%}}
.x{{font:700 13px Inter;color:#B42318}}
"""


def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="board">{body}</div></body></html>'


def head(kicker, title, lead):
    return f'<p class="kicker">Ride Rescue · Stage 3 · {kicker}</p><h1>{title}</h1><p class="lead">{lead}</p>'


def logo_system():
    v = [
        ("1 · 6", "Primary horizontal · dark backgrounds", "dk", "ride-rescue-horizontal-dark.svg", 64),
        ("1 · 5 · 9", "Horizontal · light backgrounds / navy mono", "lt", "ride-rescue-horizontal-navy.svg", 64),
        ("2", "Stacked · dark", "dk", "ride-rescue-stacked-dark.svg", 120),
        ("2", "Stacked · light", "lt", "ride-rescue-stacked-navy.svg", 120),
        ("3", "RR monogram · master (32 px +)", "dk", "rr-monogram-lime.svg", 110),
        ("11", "RR monogram · small-size cut (16–31 px)", "dk", "rr-monogram-small-lime.svg", 110),
        ("4", "Wordmark · monogram-derived R", "lt", "ride-rescue-wordmark-navy.svg", 34),
        ("10", "Monochrome lime · navy/graphite only", "gr", "ride-rescue-horizontal-lime.svg", 52),
        ("7", "One-colour black", "lt", "ride-rescue-horizontal-black.svg", 52),
        ("8", "One-colour white", "gr", "ride-rescue-horizontal-white.svg", 52),
    ]
    cells = "".join(
        f'<div class="p {bg}"><span class="lab"><span class="n">{n}</span>{t}</span><img src="{L}{f}" style="height:{h}px;max-width:90%;margin-top:14px"></div>'
        for n, t, bg, f, h in v)
    body = head("Logo system", "Lane: the logo family",
                "Every variation below is the same flat artwork recoloured. Numbers match the brief's list of 12 variations. "
                "<b>Light-background (5) and monochrome navy (9) are the same file</b>: lime fails contrast on light backgrounds, so the light version is all navy by design. "
                "<b>The promotional 3D treatment (12) is deferred to Stage 5</b>, where it belongs with the other promotional work, and it will be derived from this flat master.")
    body += f'<div class="g g2">{cells}</div>'
    return page(body)


def rules():
    misuse = [
        ("Stretched or squashed", "ride-rescue-horizontal-navy.svg", "transform:scaleX(1.25);max-width:70%"),
        ("Lime on a light background", "ride-rescue-horizontal-lime.svg", ""),
        ("Unapproved colour", "ride-rescue-horizontal-navy.svg", "filter:sepia(1) saturate(4) hue-rotate(-20deg) brightness(1.6)"),
        ("Effects (shadows, bevels, glows)", "ride-rescue-horizontal-navy.svg", "filter:drop-shadow(4px 4px 3px rgba(0,0,0,.55))"),
        ("Rotated or skewed", "ride-rescue-horizontal-navy.svg", "transform:rotate(-8deg)"),
        ("Re-set the wordmark in a font", None, ""),
    ]
    dont = ""
    for t, f, st in misuse:
        art = (f'<img src="{L}{f}" style="{st}">' if f else
               f'<div style="display:flex;align-items:center;gap:10px"><img src="{L}rr-monogram-navy.svg" style="height:44px"><span style="font:italic 700 26px Georgia">Ride Rescue</span></div>')
        dont += f'<div class="p lt dont">{art}<span class="x">✕ {t}</span></div>'
    sizes = """<table>
<tr><th>Asset</th><th>Digital minimum</th><th>Print minimum</th></tr>
<tr><td>Horizontal lockup</td><td>180 px wide</td><td>45 mm wide</td></tr>
<tr><td>Stacked lockup</td><td>100 px wide</td><td>25 mm wide</td></tr>
<tr><td>RR monogram, master</td><td>32 px tall</td><td>8 mm tall</td></tr>
<tr><td>RR monogram, small-size cut</td><td>16–31 px</td><td>5–8 mm (embroidery: 10 mm)</td></tr>
<tr><td>Wordmark alone</td><td>100 px wide</td><td>25 mm wide</td></tr></table>"""
    body = head("Construction, clear space, minimum size, misuse", "Rules that keep it consistent",
                "One unit, <b>X</b>, drives the whole system: X is the monogram's stroke, 12 units at a 64-unit mark height. "
                "Mark-to-wordmark gap is 2X in the horizontal lockup and 1.5X in the stacked one. Clear space is 2X on every side.")
    body += f"""<div class="g g2">
<div class="p lt"><span class="lab">Monogram construction · 64 / 12 / 38 grid</span><img src="../logo/diagrams/monogram-construction.svg" style="width:100%;margin-top:16px"></div>
<div class="p lt"><span class="lab">Clear space · 2X</span><img src="../logo/diagrams/clear-space-horizontal.svg" style="width:100%;margin-top:16px"></div></div>
<div class="g g2"><div class="p lt" style="display:block"><span class="lab">Minimum sizes</span><div style="margin-top:22px">{sizes}</div>
<p class="note" style="margin:14px 0 0">The horizontal lockup's minimum is set by its monogram reaching 32 px. Below 180 px wide, use the stacked lockup or the small-size monogram.</p></div>
<div class="p lt" style="display:block"><span class="lab">Small-size cut vs master</span>
<p class="note" style="margin-top:24px">The master's road closes up below 24 px. The small-size cut uses a thinner stroke (10.5), taller bowls (40) and a wider road (26 at the baseline) so the idea survives at 16 px. Use it only below 32 px, never as a replacement for the master.</p>
<div style="display:flex;gap:28px;align-items:flex-end;margin-top:10px">
<figure style="margin:0;text-align:center;font:700 11px Inter;color:{GRAY600}"><img src="../logo/png/rr-monogram-lime-on-navy-16.png" width="16"><br>master 16</figure>
<figure style="margin:0;text-align:center;font:700 11px Inter;color:{GRAY600}"><img class="px" src="../logo/png/rr-monogram-small-lime-on-navy-16.png" width="16"><br>cut 16</figure>
<figure style="margin:0;text-align:center;font:700 11px Inter;color:{GRAY600}"><img src="../logo/png/rr-monogram-lime-on-navy-16.png" width="80" style="image-rendering:pixelated"><br>master 16 at 500%</figure>
<figure style="margin:0;text-align:center;font:700 11px Inter;color:{GRAY600}"><img src="../logo/png/rr-monogram-small-lime-on-navy-16.png" width="80" style="image-rendering:pixelated"><br>cut 16 at 500%</figure></div></div></div>
<h2 style="margin-top:28px">Incorrect use</h2><div class="g g3">{dont}</div>"""
    return page(body)


def colour():
    sw = ""
    for k, (name, hx, rgb, cmyk) in CORE.items():
        dark = k in ("navy", "graphite", "gray-600")
        fg = WHITE if dark else NAVY
        sw += (f'<div class="sw"><div class="c" style="background:{hx};color:{fg}">{name}</div>'
               f'<div class="m"><b>{hx}</b><br>RGB {" ".join(map(str, rgb))}<br>CMYK {" ".join(map(str, cmyk))}</div></div>')
    tints = "".join(f'<tr><td><span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{v[0]};vertical-align:middle;border:1px solid #ccd"></span> <b>{k}</b></td><td><code>{v[0]}</code></td><td>{v[1]}</td></tr>' for k, v in TINTS.items())
    tints += "".join(f'<tr><td><span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{v[0]};vertical-align:middle"></span> <b>{k}</b> (functional)</td><td><code>{v[0]}</code></td><td>{v[1]}</td></tr>' for k, v in FUNCTIONAL.items())
    body = head("Colour", "Navy carries it, lime signals",
                "Core palette with the approved Cool Gray 600 addition. Tints are mixes of core colours for interface states only. "
                "Alert red is functional, used only for errors, never as a brand colour. CMYK values are conversions; final print values come from a press proof.")
    body += f'<div class="g g4">{sw}</div>'
    body += f"""<div class="g g2">
<div class="p lt" style="display:block"><span class="lab">Tints &amp; functional</span><table style="margin-top:22px">{tints}</table></div>
<div class="p lt" style="display:block"><span class="lab">Actions</span>
<div style="margin-top:26px"><span class="btn" style="background:{LIME};color:{NAVY}">Book a session</span><span class="btn" style="background:#A5CE33;color:{NAVY}">Hover / pressed</span>
<span class="btn" style="border:2px solid {NAVY};color:{NAVY}">Secondary</span></div>
<div style="background:{NAVY};border-radius:12px;padding:14px;margin-top:12px"><span class="btn" style="background:{LIME};color:{NAVY}">Book a session</span><span class="btn" style="border:2px solid {WHITE};color:{WHITE}">Secondary</span></div>
<p class="note" style="margin:14px 0 0">The primary action is always a lime fill with a navy label (10.2:1), on light and dark backgrounds alike. Links and ticks on light backgrounds are navy; on dark they're lime. Lime text never appears on a light background (1.35:1).</p></div></div>
<div class="g" style="grid-template-columns:3fr 2fr 1fr"><div class="p dk" style="min-height:90px"><b style="font:800 20px Manrope">Navy ~60%</b></div><div class="p" style="min-height:90px;background:{LIME}"><b style="font:800 18px Manrope">Lime ~20%</b></div><div class="p lt" style="min-height:90px"><b style="font:800 14px Manrope">White 15</b></div></div>
<p class="note">Distribution guide for brand-led surfaces (app, hero sections, vehicles). Documents and receipts invert it: mostly white, navy text, lime on the single most important element.</p>"""
    return page(body)


def type_board():
    scale = [("Display", "Manrope 800", "48 / 52", "−0.01em", "Help that knows where it's going"),
             ("H1", "Manrope 800", "36 / 40", "−0.01em", "Book a session"),
             ("H2", "Manrope 800", "28 / 34", "−0.01em", "What we fix"),
             ("H3", "Manrope 700", "20 / 26", "0", "Module programming"),
             ("Overline", "Manrope 800 caps", "12 / 16", "+0.12em", "HOW IT WORKS"),
             ("Body", "Inter 400", "16 / 26", "0", "We back up every module before a single value changes."),
             ("UI label", "Inter 600", "14 / 20", "0", "Preferred contact"),
             ("Numbers", "Inter 700 tnum", "20 / 24", "0", "$145.00 · ETA 18 min")]
    rows = ""
    for role, face, size, track, ex in scale:
        fam = "Manrope" if "Manrope" in face else "Inter"
        w = 800 if "800" in face else 700 if "700" in face else 600 if "600" in face else 400
        px = int(size.split(" / ")[0])
        tt = "uppercase" if "caps" in face else "none"
        ls = track.replace("−", "-") if track != "0" else "0"
        rows += (f'<tr><td style="width:110px"><b>{role}</b><br><span style="color:{GRAY600};font-size:12px">{face}<br>{size} · {track}</span></td>'
                 f'<td style="font-family:{fam};font-weight:{w};font-size:{min(px, 40)}px;letter-spacing:{ls};text-transform:{tt};font-feature-settings:\'tnum\'">{ex}</td></tr>')
    body = head("Typography", "Two families, one voice",
                "Manrope (brand, headings, labels, the wordmark's base) and Inter (body, interface, numbers). Both are SIL Open Font License 1.1: free for commercial print, web, app and vehicle use. Self-host the WOFF2 files; don't rely on a font CDN.")
    body += f"""<div class="g g2">
<div class="p dk" style="display:block"><span class="lab">Manrope · brand</span><div style="font:800 64px/1 Manrope;margin-top:26px">Aa Rr</div>
<div style="font:400 18px Manrope;margin-top:12px;color:#c9d3dc">200 300 400 500 600 700 <b style="font-weight:800;color:{LIME}">800</b></div>
<div style="font:800 15px Manrope;letter-spacing:.12em;margin-top:14px">ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789</div></div>
<div class="p lt" style="display:block"><span class="lab">Inter · interface</span><div style="font:600 64px/1 Inter;margin-top:26px">Aa 18</div>
<div style="font:400 18px Inter;margin-top:12px;color:{GRAY600}">400 Regular · 500 Medium · <b>600 Semibold</b> · <b style="font-weight:700">700 Bold</b></div>
<div style="font:600 15px Inter;margin-top:14px;font-feature-settings:'tnum'">Tabular: 1111.00 / 8888.00 line up</div></div></div>
<div class="p lt" style="display:block"><span class="lab">Scale (desktop; mobile steps H1→28, Display→36)</span><table style="margin-top:20px">{rows}</table></div>"""
    return page(body)


def icon_board():
    cells = "".join(
        f'<div class="p lt" style="flex-direction:column;gap:10px;min-height:150px">{icon_mod.svg(k, 48, NAVY)}'
        f'<div style="display:flex;gap:10px;align-items:center;background:{NAVY};border-radius:8px;padding:6px 10px">{icon_mod.svg(k, 24, LIME)}{icon_mod.svg(k, 16, LIME)}</div>'
        f'<span style="font:700 12px Inter;text-align:center">{label}</span></div>'
        for k, (label, _) in icon_mod.ICONS.items())
    grid = (f'<svg width="220" height="220" viewBox="0 0 24 24"><g stroke="#D99B67" stroke-width=".05">'
            + "".join(f'<line x1="{i}" x2="{i}" y1="0" y2="24"/><line y1="{i}" y2="{i}" x1="0" x2="24"/>' for i in range(25))
            + '</g><rect x="2" y="2" width="20" height="20" fill="none" stroke="#B9E532" stroke-width=".15"/>'
            + f'<g fill="none" stroke="{NAVY}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".85">{icon_mod.ICONS["breakdown"][1]}</g></svg>')
    body = head("Iconography", "Seventeen services, one drawing style",
                "The brief's 12 roadside icons plus 5 for the diagnostics, programming and service work Ride Rescue sells today. "
                "24-unit grid, 2-unit live-area padding, 2-unit stroke, round caps and joins, 2-unit corner radius. Vehicles face right (the direction of travel), and wheels are always r2 on y17. Icons inherit text colour.")
    body += f"""<div class="g" style="grid-template-columns:260px 1fr"><div class="p lt">{grid}</div><div class="p lt" style="display:block"><span class="lab">Rules</span><ul class="note" style="margin-top:26px;line-height:1.8"><li>Navy on light, lime or Soft White on navy. Never lime on light.</li><li>Use at 16, 20, 24, 32 or 48 px. Scale only the whole icon; never change the stroke.</li><li>One idea per icon. Badges (bolt, clock, plus) sit inside the live area.</li><li>New icons start from an existing one's vehicle, wheel or box so proportions stay shared.</li><li>Icons label services; they don't decorate. Pair each with a text label in UI.</li></ul></div></div>"""
    body += f'<div class="g g4">{cells}</div>'
    return page(body)


def graphics_board():
    body = head("Graphic language", "Everything comes from the lane",
                "The supporting graphics are cut from the logo's own negative space and grid, so they reinforce the mark instead of competing with it. No stock car photos as a substitute, no racing stripes, and no checker or chevron patterns (see the emergency-vehicle note in Stage 1).")
    hero = f"""<div class="p dk" style="min-height:300px;overflow:hidden;justify-content:flex-start;align-items:flex-end;padding:36px">
<img src="../graphics/lane-wedge-raised.svg" style="position:absolute;right:60px;bottom:0;height:300px">
<div style="position:relative"><p style="font:800 12px Manrope;letter-spacing:.14em;color:{LIME};margin:0 0 8px">ROADSIDE · DIAGNOSTICS · PROGRAMMING</p>
<p style="font:800 36px/1.1 Manrope;margin:0;max-width:560px">Help that knows where it's going.</p>
<img src="../graphics/lane-divider-lime.svg" style="width:220px;height:6px;margin-top:18px;display:block"></div></div>"""
    body += f'<div class="g">{hero}</div>'
    body += f"""<div class="g g4">
<div class="p dk"><span class="lab">Lane wedge</span><img src="../graphics/lane-wedge-lime.svg" style="height:120px;margin-top:14px"></div>
<div class="p dk" style="background:url(../graphics/pattern-road-tile.svg);background-size:96px 48px"><span class="lab">Road-marking pattern</span></div>
<div class="p lt" style="flex-direction:column;gap:14px"><span class="lab">Lane divider</span><img src="../graphics/lane-divider-navy.svg" style="width:85%;height:6px;margin-top:16px"><span class="note" style="font-size:12px">Tapered rule: section breaks</span></div>
<div class="p lt"><span class="lab">Cut-corner frame</span><img src="../graphics/cut-corner-frame.svg" style="width:85%;margin-top:14px"></div></div>
<div class="p lt" style="display:block"><span class="lab">How to use them</span><ul class="note" style="margin-top:24px;line-height:1.8">
<li><b>Lane wedge</b>: the logo's negative space, extracted. Use it large, always running off the top edge toward the horizon, in Navy Raised on navy (lime only at small sizes), as the one hero accent. Never more than one per layout, never rotated, never beside the logo at a similar size.</li>
<li><b>Road-marking pattern</b>: staggered dashes on the 12-unit rhythm. Use it as a quiet background for app loading screens, social banners and the back of business cards, in navy-raised on navy only.</li>
<li><b>Lane divider</b>: a tapered rule for section breaks and under headings. Navy on light, lime on dark.</li>
<li><b>Direction wedge</b> (<code>graphics/direction-wedge-*.svg</code>): the wedge turned to point right. Use it for "next step" cues in place of generic arrows.</li>
<li><b>Cut-corner frame</b>: panels and photo crops with the top-right corner clipped at 45°, with the cut equal to 2X at the panel scale. It works like the clipped corner of a road-sign plate. One per view.</li></ul></div>"""
    return page(body)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("01-logo-system", logo_system), ("02-logo-rules", rules), ("03-colour", colour),
                     ("04-typography", type_board), ("05-iconography", icon_board), ("06-graphic-language", graphics_board)):
        with open(os.path.join(OUT, f"{name}.html"), "w") as f:
            f.write(fn())
    print("stage 3 boards written")


if __name__ == "__main__":
    main()
