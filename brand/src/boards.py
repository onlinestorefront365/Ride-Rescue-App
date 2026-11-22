"""Presentation boards for the Stage 2 monogram concepts (HTML, rendered by render.js)."""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "exploration", "stage-2")

NAVY, LIME, WHITE, AMBER, GRAPHITE, GRAY = "#14283D", "#B9E532", "#F5F6F2", "#D99B67", "#252A30", "#87929D"

NOTES = {
    "a-tandem": {
        "letter": "A",
        "idea": "Two upright R's in sequence. The first R's leg runs forward and locks into the foot of the second: two letters, one connected unit.",
        "scores": {"Letter recognition": 5, "Ownability": 2, "Small-size performance": 5, "Brand fit": 3},
        "verdict": "Clear and dependable, but it reads like RR typed in a bold geometric font. Easy to read, hard to own.",
    },
    "b-lane": {
        "letter": "B",
        "idea": "A mirrored pair whose stems lean apart. The space between them becomes a road running to a vanishing point: the road ahead, held by two R's.",
        "scores": {"Letter recognition": 4, "Ownability": 5, "Small-size performance": 3, "Brand fit": 5},
        "verdict": "Recommended. Symmetry reads as stable and trustworthy, and the road is real negative space rather than an added graphic. The master reads down to 32 px; below that it needs a simplified small-size cut.",
    },
    "c-route": {
        "letter": "C",
        "idea": "One continuous monoline path traced like a route on a map, from an origin dot up the first R and through the second to the baseline.",
        "scores": {"Letter recognition": 4, "Ownability": 3, "Small-size performance": 3, "Brand fit": 3},
        "verdict": "Most approachable and app-like, but monoline marks are common among tech start-ups, and the thin line and dot soften at 32 px.",
    },
}

CSS = f"""
*{{box-sizing:border-box}}
body{{margin:0;background:{WHITE};color:{NAVY};font-family:Manrope,system-ui,sans-serif;width:1200px}}
@font-face{{font-family:Manrope;src:url(../../fonts/Manrope-Variable.ttf);font-weight:200 800}}
.board{{padding:48px}}
.kicker{{font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:{GRAY};margin:0 0 6px}}
h1{{font-size:40px;font-weight:800;margin:0 0 8px;letter-spacing:-.01em}}
.idea{{font-size:18px;line-height:1.5;max-width:880px;margin:0 0 28px;color:{GRAPHITE}}}
.row{{display:grid;gap:16px;margin-bottom:16px}}
.r2{{grid-template-columns:1fr 1fr}}
.panel{{border-radius:16px;padding:32px;display:flex;align-items:center;justify-content:center;min-height:260px;position:relative}}
.light{{background:#fff;border:1px solid #dfe3e6}}
.dark{{background:{NAVY};color:{WHITE}}}
.label{{position:absolute;left:16px;top:12px;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:{GRAY}}}
.dark .label{{color:#8fa0b3}}
.big img{{height:180px}}
.cons img{{width:100%}}
.ladder{{display:flex;align-items:flex-end;gap:24px;flex-wrap:wrap}}
.ladder figure{{margin:0;text-align:center;font-size:12px;font-weight:700;color:{GRAY}}}
.ladder img{{display:block;margin:0 auto 6px}}
.px{{image-rendering:pixelated}}
.lock img{{height:84px;max-width:100%}}
table{{border-collapse:collapse;width:100%;font-size:15px}}
td{{padding:8px 0;border-bottom:1px solid #e3e6e8}}
.dots span{{display:inline-block;width:14px;height:14px;border-radius:50%;margin-right:5px;background:#d9dee2}}
.dots span.on{{background:{NAVY}}}
.verdict{{font-size:16px;line-height:1.55;margin:0}}
.rec{{background:{LIME};color:{NAVY};font-weight:800;border-radius:999px;padding:4px 12px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin-left:10px;vertical-align:middle}}
.trio{{grid-template-columns:repeat(3,1fr)}}
.trio .panel{{flex-direction:column;gap:18px;min-height:240px}}
.trio .panel img.m{{height:110px}}
.cap{{font-size:15px;font-weight:800}}
.small{{display:flex;gap:14px;align-items:flex-end}}
"""


def dots(n):
    return "".join(f'<span class="{"on" if i < n else ""}"></span>' for i in range(5))


def concept_board(key, c):
    n = NOTES[key]
    f = c["files"]
    rec = '<span class="rec">Recommended</span>' if key == "b-lane" else ""
    ladder = "".join(
        f'<figure><img src="png/{key}-app-{s}.png" width="{s}" height="{s}">{s} px</figure>' for s in (128, 64, 32))
    ladder += f'<figure><img class="px" src="png/{key}-app-32.png" width="128" height="128">32 px at 400%</figure>'
    ladder += f'<figure><img src="png/{key}-mark-navy-32.png" width="32" style="height:auto">mark only, 32 px</figure>'
    rows = "".join(f"<tr><td>{k}</td><td class='dots' style='text-align:right'>{dots(v)}</td></tr>" for k, v in n["scores"].items())
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="board">
<p class="kicker">Ride Rescue · Stage 2 · RR monogram concept {n['letter']}</p>
<h1>{c['name']}{rec}</h1>
<p class="idea">{n['idea']}</p>
<div class="row r2 big">
  <div class="panel light"><span class="label">Navy on white</span><img src="{key}/{f['mark-navy']}"></div>
  <div class="panel dark"><span class="label">Lime on navy</span><img src="{key}/{f['mark-lime']}"></div>
</div>
<div class="row r2">
  <div class="panel light cons"><span class="label">Construction · 64-unit cap · 12-unit stroke</span><img src="{key}/{f['construction']}"></div>
  <div class="panel light"><span class="label">App tile size test · actual pixels</span><div class="ladder">{ladder}</div></div>
</div>
<div class="row r2 lock">
  <div class="panel light"><span class="label">Primary lockup · light</span><img src="{key}/{f['lockup-light']}"></div>
  <div class="panel dark"><span class="label">Primary lockup · dark</span><img src="{key}/{f['lockup-dark']}"></div>
</div>
<div class="row r2">
  <div class="panel light" style="display:block"><span class="label">Evaluation</span><table style="margin-top:18px">{rows}</table></div>
  <div class="panel light" style="display:block"><span class="label">Verdict</span><p class="verdict" style="margin-top:22px">{n['verdict']}</p></div>
</div>
</div></body></html>"""


def overview(m):
    cells = ""
    for key, c in m["concepts"].items():
        n = NOTES[key]
        rec = '<span class="rec">Recommended</span>' if key == "b-lane" else ""
        cells += f"""<div class="panel dark"><img class="m" src="{key}/{c['files']['mark-lime']}">
<div class="cap">{n['letter']} · {c['name']}{rec}</div>
<div class="small"><img src="png/{key}-app-64.png" width="64"><img src="png/{key}-app-32.png" width="32"><img class="px" src="png/{key}-app-32.png" width="64"></div></div>"""
    light = "".join(f'<div class="panel light"><img class="m" src="{k}/{c["files"]["mark-navy"]}"></div>' for k, c in m["concepts"].items())
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="board">
<p class="kicker">Ride Rescue · Stage 2</p>
<h1>Three RR monogram directions</h1>
<p class="idea">Same 64-unit cap height and 12-unit stroke, three different ideas. Shown in lime on navy and navy on white, with the app tile at 64 px, at 32 px, and at 32 px enlarged to show the pixels.</p>
<div class="row trio">{cells}</div>
<div class="row trio">{light}</div>
</div></body></html>"""


def main():
    m = json.load(open(os.path.join(OUT, "manifest.json")))
    for key, c in m["concepts"].items():
        open(os.path.join(OUT, f"board-{key}.html"), "w").write(concept_board(key, c))
    open(os.path.join(OUT, "board-overview.html"), "w").write(overview(m))
    print("boards written")


if __name__ == "__main__":
    main()
