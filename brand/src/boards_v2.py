"""Identity v2 presentation boards (HTML → PNG/PDF via render_v2.js)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import icons as icon_mod
from build_v2 import CORE, DERIVED, FUNCTIONAL, TAGLINE

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "identity", "boards")
L, PR, PNG, G = "../logo/svg/", "../logo/promo/", "../logo/png/", "../graphics/"
BLUE, SILVER, CARBON, WHITE, STEEL, ACTION = "#087FFF", "#C3C9D0", "#111315", "#FFFFFF", "#73777C", "#0973E5"

CSS = f"""
@font-face{{font-family:Saira;src:url(../../fonts/Saira-Italic-Variable.ttf);font-style:italic;font-weight:100 900;font-stretch:50% 125%}}
@font-face{{font-family:Inter;src:url(../../fonts/Inter-Variable.ttf);font-weight:100 900}}
*{{box-sizing:border-box}}
body{{margin:0;background:#E9ECEF;color:{CARBON};font-family:Inter,sans-serif;width:1200px}}
.board{{padding:48px}}
.kicker{{font:italic 700 14px Saira;font-stretch:112%;letter-spacing:.14em;text-transform:uppercase;color:{STEEL};margin:0 0 6px}}
h1{{font:italic 800 44px/1.05 Saira;font-stretch:112%;margin:0 0 10px}}
h2{{font:italic 800 20px Saira;font-stretch:112%;margin:0 0 12px}}
.lead{{font-size:16.5px;line-height:1.55;max-width:920px;margin:0 0 26px;color:#2a2e33}}
.g{{display:grid;gap:14px;margin-bottom:14px}}
.g2{{grid-template-columns:1fr 1fr}} .g3{{grid-template-columns:repeat(3,1fr)}} .g4{{grid-template-columns:repeat(4,1fr)}}
.p{{border-radius:14px;padding:26px;position:relative;display:flex;align-items:center;justify-content:center;min-height:170px}}
.lt{{background:#fff;border:1px solid #d7dbdf}} .dk{{background:{CARBON};color:#fff}} .bl{{background:{BLUE}}}
.lab{{position:absolute;left:14px;top:10px;font:700 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:{STEEL}}}
.dk .lab{{color:#9aa1a9}} .bl .lab{{color:#fff}}
.tag{{display:inline-block;background:{BLUE};color:#fff;font:700 11px Inter;border-radius:999px;padding:2px 8px;margin-right:6px}}
.note{{font-size:14px;line-height:1.55;color:#2a2e33}}
.dk .note{{color:#c3c9d0}}
table{{border-collapse:collapse;width:100%;font-size:14px}} td,th{{padding:7px 8px;border-bottom:1px solid #e3e6e8;text-align:left;vertical-align:top}}
th{{font:700 11px Inter;letter-spacing:.08em;text-transform:uppercase;color:{STEEL}}}
.sw{{border-radius:12px;overflow:hidden;border:1px solid #d7dbdf;background:#fff}}
.sw .c{{height:120px;display:flex;align-items:flex-end;padding:12px;font:italic 800 17px Saira;font-stretch:112%}}
.sw .m{{padding:12px;font-size:12.5px;line-height:1.6;font-feature-settings:"tnum"}}
.btn{{display:inline-flex;padding:12px 20px;border-radius:8px;font:700 15px Inter;margin:4px}}
.lad{{display:flex;gap:22px;align-items:flex-end;flex-wrap:wrap}}
.lad figure{{margin:0;text-align:center;font:700 11px Inter;color:{STEEL}}} .lad img{{display:block;margin:0 auto 6px}}
.px{{image-rendering:pixelated}}
.dont{{flex-direction:column;gap:12px}} .dont img{{max-height:90px;max-width:80%}}
.x{{font:700 13px Inter;color:#C4320A}}
"""


def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="board">{body}</div></body></html>'


def head(k, t, lead):
    return f'<p class="kicker">Ride Rescue · Identity v2 · {k}</p><h1>{t}</h1><p class="lead">{lead}</p>'


def p(cls, label, inner, style=""):
    return f'<div class="p {cls}" style="{style}"><span class="lab">{label}</span>{inner}</div>'


def img(src, h=None, w=None, extra=""):
    s = (f"height:{h}px;" if h else "") + (f"width:{w};" if w else "") + "max-width:92%;margin-top:14px;" + extra
    return f'<img src="{src}" style="{s}">'


def logo_system():
    b = head("Logo system", "The RR is the identity",
             "Four levels, one construction. The <b>primary</b> carries the full story: RR, a 12-point ratcheting wrench, Oregon peaks and the blue arc. "
             "The <b>secondary</b> drops the scenery. The <b>micro mark</b> is the RR alone, and it is what people should come to recognise. "
             "The wrench and mountains support the RR; they never appear without it.")
    b += '<div class="g g2">' + p("dk", '<span class="tag">Primary</span>Stacked lockup', img(L + "ride-rescue-stacked-dark.svg", 330), "min-height:400px") \
         + '<div style="display:grid;gap:14px">' \
         + p("dk", '<span class="tag">Primary</span>Horizontal lockup', img(L + "ride-rescue-horizontal-dark.svg", None, "92%")) \
         + p("lt", "Horizontal · light", img(L + "ride-rescue-horizontal-light.svg", None, "92%")) + '</div></div>'
    b += '<div class="g g4">' \
         + p("dk", '<span class="tag">Secondary</span>RR in wrench', img(L + "rr-wrench-dark.svg", 140)) \
         + p("lt", "Secondary · light", img(L + "rr-wrench-light.svg", 140)) \
         + p("dk", '<span class="tag">Micro</span>RR monogram', img(L + "rr-micro-white.svg", 70)) \
         + p("bl", "Micro on blue", img(L + "rr-micro-white.svg", 70)) + '</div>'
    b += '<div class="g g3">' \
         + p("dk", "Compact horizontal (headers)", img(L + "ride-rescue-horizontal-compact-dark.svg", None, "92%")) \
         + p("lt", "Wordmark + tagline", img(L + "ride-rescue-wordmark-tagline-light.svg", None, "92%")) \
         + p("dk", "Wordmark", img(L + "ride-rescue-wordmark-dark.svg", None, "88%")) + '</div>'
    b += '<div class="g g4">' \
         + p("lt", "One colour · black", img(L + "ride-rescue-stacked-black.svg", 150)) \
         + p("dk", "One colour · white", img(L + "ride-rescue-stacked-white.svg", 150)) \
         + p("lt", "Emblem · light", img(L + "emblem-light.svg", 150)) \
         + p("dk", "Emblem · dark", img(L + "emblem-dark.svg", 150)) + '</div>'
    return page(b)


def promo():
    b = head("Promotional treatment", "Chrome is for show, not for the master",
             "The metallic version is generated from the flat master: same paths, with gradients, bevel lighting and a glow added on top. "
             "Use it for website banners, ads, presentations, video and merchandise mockups. Never use it for the app icon, favicon, vinyl, embroidery, "
             "single-colour print or anything under 200 px wide. If the chrome version and the flat version ever disagree, the flat version is right.")
    b += '<div class="g">' + p("dk", "Stacked · chrome", img(PNG + "ride-rescue-stacked-chrome.png", 560), "padding:0;background:#000") + '</div>'
    b += '<div class="g g2">' + p("dk", "Emblem · chrome", img(PNG + "emblem-chrome.png", 300), "padding:0;background:#000") \
         + p("dk", "Horizontal · chrome", img(PNG + "ride-rescue-horizontal-chrome.png", None, "96%"), "padding:0;background:#000") + '</div>'
    return page(b)


def rules():
    lad = lambda items: '<div class="lad">' + "".join(
        f'<figure><img class="{c}" src="{PNG}{f}" width="{w}">{t}</figure>' for f, w, t, c in items) + "</div>"
    micro = lad([("tile-micro-16.png", 16, "16", ""), ("tile-micro-24.png", 24, "24", ""), ("tile-micro-32.png", 32, "32", ""),
                 ("tile-micro-48.png", 48, "48", ""), ("tile-micro-16.png", 96, "16 at 600%", "px")])
    sec = lad([("tile-wrench-48.png", 48, "48", ""), ("tile-wrench-64.png", 64, "64", ""), ("tile-wrench-96.png", 96, "96", ""),
               ("tile-wrench-48.png", 144, "48 at 300%", "px")])
    emb = lad([("tile-emblem-64.png", 64, "64", ""), ("tile-emblem-96.png", 96, "96", ""), ("tile-emblem-128.png", 128, "128", ""),
               ("tile-emblem-64.png", 128, "64 at 200%", "px")])
    sizes = """<table><tr><th>Asset</th><th>Digital min</th><th>Print min</th><th>Below that, use</th></tr>
<tr><td>Micro mark (RR)</td><td>16 px</td><td>5 mm tall</td><td>—</td></tr>
<tr><td>Secondary (RR in wrench)</td><td>64 px</td><td>16 mm</td><td>Micro mark</td></tr>
<tr><td>Primary emblem (with peaks)</td><td>96 px</td><td>25 mm</td><td>Secondary</td></tr>
<tr><td>Stacked lockup</td><td>200 px wide</td><td>50 mm wide</td><td>Secondary + wordmark</td></tr>
<tr><td>Horizontal lockup</td><td>280 px wide</td><td>70 mm wide</td><td>Compact horizontal</td></tr>
<tr><td>Compact horizontal</td><td>180 px wide</td><td>45 mm wide</td><td>Micro mark</td></tr></table>"""
    misuse = [("Wrench without the RR", "dont-wrench-only.svg"), ("Stretched", "ride-rescue-horizontal-light.svg"),
              ("Recoloured outside the palette", "ride-rescue-horizontal-light.svg"), ("Chrome version in one-colour use", None),
              ("Electric Blue body text on white", None), ("RR rebuilt in a font", None)]
    styles = ["", "transform:scaleX(.62)", "filter:hue-rotate(140deg) saturate(2)", "", "", ""]
    dont = ""
    for (t, f), st in zip(misuse, styles):
        if f == "dont-wrench-only.svg":
            art = f'<img src="{G}wrench-only.svg" style="height:100px">'
        elif f:
            art = f'<img src="{L}{f}" style="{st};max-height:70px">'
        elif t.startswith("Chrome"):
            art = f'<img src="{PNG}emblem-chrome.png" style="height:90px;filter:grayscale(1) contrast(3)">'
        elif t.startswith("Electric"):
            art = f'<p style="color:{BLUE};font-size:15px;margin:0;max-width:240px">Book your diagnostic session today and we will confirm a time.</p>'
        else:
            art = '<span style="font:italic 900 56px Arial;letter-spacing:-2px">RR</span>'
        dont += f'<div class="p lt dont">{art}<span class="x">✕ {t}</span></div>'
    b = head("Construction, size and misuse", "Rules that keep it one company",
             "The R is drawn upright from rounded-square parts on a 64-unit grid with a 16-unit stroke, the system unit <b>X</b>, then slanted 12°, Saira Italic's own angle. "
             "The first R's leg runs on as a road line under the second R and out past it. "
             "Clear space around every lockup is 1X measured at the RR's size; around the micro mark it is 2X.")
    b += '<div class="g g2">' + p("lt", "Upright R construction", img("../logo/diagrams/r-construction-upright.svg", 210)) \
         + p("lt", "RR: slant and road line", img("../logo/diagrams/rr-construction.svg", 180)) + '</div>'
    b += '<div class="g g3">' + p("dk", "Micro mark · actual pixels", micro, "display:block;padding-top:40px") \
         + p("dk", "Secondary · actual pixels", sec, "display:block;padding-top:40px") \
         + p("dk", "Primary emblem · actual pixels", emb, "display:block;padding-top:40px") + '</div>'
    b += '<div class="g">' + p("lt", "Minimum sizes", f'<div style="margin-top:20px;width:100%">{sizes}</div>', "display:block") + '</div>'
    b += f'<h2 style="margin-top:24px">Incorrect use</h2><div class="g g3">{dont}</div>'
    return page(b)


def colour():
    sw = ""
    for k, (name, hx, rgb, cmyk) in CORE.items():
        fg = WHITE if k in ("carbon-black", "electric-blue") else CARBON
        sw += (f'<div class="sw"><div class="c" style="background:{hx};color:{fg};{"border-bottom:1px solid #d7dbdf" if k == "white" else ""}">{name}</div>'
               f'<div class="m"><b>{hx}</b><br>RGB {" ".join(map(str, rgb))}<br>CMYK {" ".join(map(str, cmyk))}</div></div>')
    der = "".join(f'<tr><td><span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{v[0]};vertical-align:middle;border:1px solid #ccd"></span> <b>{k}</b></td><td><code>{v[0]}</code></td><td>{v[1]}</td></tr>' for k, v in DERIVED.items())
    der += "".join(f'<tr><td><span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{v[0]};vertical-align:middle"></span> <b>{k}</b></td><td><code>{v[0]}</code></td><td>{v[1]} (functional only)</td></tr>' for k, v in FUNCTIONAL.items())
    contrast = """<table><tr><th>Pair</th><th>Ratio</th><th>Verdict</th></tr>
<tr><td>White on Carbon</td><td>18.62</td><td>All text</td></tr>
<tr><td>Steel Silver on Carbon</td><td>11.16</td><td>All text</td></tr>
<tr><td>Electric Blue on Carbon</td><td>4.87</td><td>All text (AA)</td></tr>
<tr><td>Carbon on Electric Blue</td><td>4.87</td><td>Button labels on dark</td></tr>
<tr><td>White on Electric Blue</td><td>3.83</td><td><b>Large text only</b>: fails body/button text</td></tr>
<tr><td>Electric Blue on White</td><td>3.83</td><td><b>Large text and logo only</b></td></tr>
<tr><td>White on Action Blue</td><td>4.57</td><td>Buttons on light (AA)</td></tr>
<tr><td>Steel Silver on White</td><td>1.67</td><td><b>Fails</b>: never text; use Steel 600</td></tr></table>"""
    b = head("Colour", "Carbon, steel, one electric signal",
             "Your four colours are the brand. Six derived values (each mixed from those four) solve the two places the raw palette fails: "
             "white button text on Electric Blue, and anything silver on white. CMYK values are conversions. Electric Blue sits outside the CMYK gamut and prints duller, "
             "so vehicles and signage need a spot or vinyl match picked from a physical swatch.")
    b += f'<div class="g g4">{sw}</div>'
    b += '<div class="g g2">' + p("lt", "Derived & functional", f'<table style="margin-top:20px">{der}</table>', "display:block") \
         + p("lt", "Contrast", f'<div style="margin-top:20px">{contrast}</div>', "display:block") + '</div>'
    btn = (f'<span class="btn" style="background:{ACTION};color:#fff">Book a session</span>'
           f'<span class="btn" style="border:2px solid {CARBON};color:{CARBON}">Secondary</span>')
    btn_dk = (f'<span class="btn" style="background:{BLUE};color:{CARBON}">Book a session</span>'
              f'<span class="btn" style="border:2px solid #fff;color:#fff">Secondary</span>')
    b += '<div class="g g2">' + p("lt", "Actions on light", f'<div style="margin-top:18px">{btn}</div>') + p("dk", "Actions on dark", f'<div style="margin-top:18px">{btn_dk}</div>') + '</div>'
    b += '<div class="g" style="grid-template-columns:6fr 2fr 1.5fr 0.5fr"><div class="p dk" style="min-height:80px"><b style="font:italic 800 20px Saira">Carbon ~60%</b></div>' \
         f'<div class="p" style="min-height:80px;background:{SILVER}"><b style="font:italic 800 16px Saira">Steel 20%</b></div>' \
         f'<div class="p lt" style="min-height:80px"><b style="font:italic 800 14px Saira">White 15</b></div>' \
         f'<div class="p" style="min-height:80px;background:{BLUE}"></div></div><p class="note">Electric Blue is the signal: about 5% of any surface, on the one thing that matters most.</p>'
    return page(b)


def typography():
    scale = [("Display", "Saira Italic 800 · wdth 112", "52 / 54", "0", "MOBILE DIAGNOSTICS"),
             ("H1", "Saira Italic 800 · wdth 112", "36 / 40", "0", "Book a session"),
             ("H2", "Saira Italic 700 · wdth 112", "28 / 32", "0", "What we fix"),
             ("Overline / tagline", "Saira Italic 600 · caps", "13 / 16", "+0.16em", "PROGRAMMING • REPAIRS"),
             ("H3", "Inter 700", "20 / 26", "0", "Module programming"),
             ("Body", "Inter 400", "16 / 26", "0", "We back up every module before a single value changes."),
             ("UI label", "Inter 600", "14 / 20", "0", "Preferred contact"),
             ("Numbers", "Inter 700 tnum", "20 / 24", "0", "$145.00 · ETA 18 min")]
    rows = ""
    for role, face, size, tr, ex in scale:
        px = int(size.split(" / ")[0])
        if "Saira" in face:
            w = 800 if "800" in face else 700 if "700" in face else 600
            st = f"font:italic {w} {min(px, 40)}px Saira;font-stretch:112%;letter-spacing:{'0.16em' if 'caps' in face else '0'}"
        else:
            w = 700 if "700" in face else 600 if "600" in face else 400
            st = f"font:{w} {min(px, 40)}px Inter;font-feature-settings:'tnum'"
        rows += f'<tr><td style="width:150px"><b>{role}</b><br><span style="color:{STEEL};font-size:12px">{face}<br>{size} · {tr}</span></td><td style="{st}">{ex}</td></tr>'
    b = head("Typography", "Industrial italic, honest body",
             "Saira Italic (SIL OFL 1.1) is the voice: slightly slanted, squared and heavy, for the wordmark, headlines and the tagline. "
             "Inter stays for body copy, forms and numbers, upright for long-form reading. Saira's width axis is set to 112 for display. "
             "The wordmark's R's are the monogram's R, not Saira's.")
    b += '<div class="g g2">' + p("dk", "Saira Italic · display",
                                    f'<div style="margin-top:20px;width:100%"><div style="font:italic 800 64px/1 Saira;font-stretch:112%">Aa Rr 18</div>'
                                    f'<div style="font:italic 600 14px Saira;letter-spacing:.16em;margin-top:14px;color:{SILVER}">{TAGLINE}</div>'
                                    f'<div style="font:italic 500 16px Saira;margin-top:10px;color:#9aa1a9">300 · 400 · 500 · 600 · 700 · <b style="color:{BLUE}">800</b></div></div>', "display:block") \
         + p("lt", "Inter · interface",
             f'<div style="margin-top:20px"><div style="font:600 64px/1 Inter">Aa 18</div>'
             f'<div style="font:400 16px Inter;margin-top:14px;color:{STEEL}">400 · 500 · <b>600</b> · <b style="font-weight:700">700</b> · tabular 1111.00 / 8888.00</div></div>', "display:block") + '</div>'
    b += p("lt", "Scale", f'<table style="margin-top:18px">{rows}</table>', "display:block")
    return page(b)


def icons_graphics():
    cells = "".join(
        f'<div class="p lt" style="flex-direction:column;gap:8px;min-height:130px">{icon_mod.svg(k, 40, CARBON)}'
        f'<div style="display:flex;gap:8px;align-items:center;background:{CARBON};border-radius:8px;padding:6px 10px">{icon_mod.svg(k, 24, SILVER)}{icon_mod.svg(k, 16, BLUE)}</div>'
        f'<span style="font:700 11.5px Inter;text-align:center">{label}</span></div>'
        for k, (label, _) in icon_mod.ICONS.items())
    hero = (f'<div class="p dk" style="min-height:300px;overflow:hidden;background:url({G}carbon-fibre-tile.svg) 0 0/16px 16px;justify-content:flex-start;align-items:flex-end;padding:36px">'
            f'<img src="{G}ridge-band-raised.svg" style="position:absolute;left:0;bottom:0;width:100%">'
            f'<img src="{G}ratchet-ring-raised.svg" style="position:absolute;right:-90px;top:-90px;height:300px">'
            f'<img src="{G}swoosh-blue.svg" style="position:absolute;right:150px;top:36px;height:200px">'
            f'<div style="position:relative"><p style="font:italic 600 13px Saira;letter-spacing:.16em;color:{BLUE};margin:0 0 8px">MOBILE DIAGNOSTICS • PROGRAMMING • REPAIRS</p>'
            f'<p style="font:italic 800 42px/1.05 Saira;font-stretch:112%;margin:0;max-width:620px">Dealer-level programming. Without the dealer.</p>'
            f'<img src="{G}road-line-blue.svg" style="width:300px;height:5px;margin-top:16px;display:block"></div></div>')
    b = head("Icons & graphic language", "Supporting cast",
             "The 17 service icons carry over unchanged in drawing and are recoloured: carbon on light, silver on dark, Electric Blue only for the active or selected state. "
             "Supporting graphics are cut from the emblem itself: the road line, the arc, the ridge and the 12-point ratchet ring. Carbon fibre is a texture for promotional and background use only. They support the RR; none of them is ever used as a logo.")
    b += '<div class="g">' + hero + '</div>'
    b += f'<div class="g g4">' \
         + p("dk", "Road line", f'<img src="{G}road-line-blue.svg" style="width:85%;height:8px;margin-top:14px">') \
         + p("dk", "Arc", img(G + "swoosh-blue.svg", 120)) \
         + p("dk", "Ridge (horizon band)", img(G + "ridge-band-silver.svg", None, "92%")) \
         + p("dk", "12-point ratchet ring", img(G + "ratchet-ring-silver.svg", 110)) + '</div>'
    b += f'<div class="g" style="grid-template-columns:repeat(6,1fr)">{cells}</div>'
    return page(b)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("01-logo-system", logo_system), ("02-promotional", promo), ("03-rules", rules),
                     ("04-colour", colour), ("05-typography", typography), ("06-icons-graphics", icons_graphics)):
        with open(os.path.join(OUT, f"{name}.html"), "w") as f:
            f.write(fn())
    print("v2 boards written")


if __name__ == "__main__":
    main()
