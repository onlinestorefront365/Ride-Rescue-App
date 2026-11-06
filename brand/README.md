# Ride Rescue — Brand Identity

| Stage | Status | Files |
|---|---|---|
| 1 · Creative strategy | Positioning still applies; colour, type and logo direction superseded by v2 | [`01-creative-strategy.md`](01-creative-strategy.md) |
| 2 · Logo development | Lane chosen, later replaced by v2 | [`02-monogram-concepts.md`](02-monogram-concepts.md), [`exploration/stage-2/`](exploration/stage-2/) |
| 3 · Identity system **v2** | Built, awaiting approval | [`03-identity-system.md`](03-identity-system.md), [`identity/`](identity/) |
| Archived: Lane v1 | Still used by the live website until v2 is approved | [`archive/lane-v1/`](archive/lane-v1/) |
| 4 · Digital assets | Not started | — |
| 5 · Physical applications | Not started | — |
| 6 · Final production | Not started | — |

## Folder layout

```
brand/
  01-creative-strategy.md     positioning (colour/type sections superseded by v2)
  02-monogram-concepts.md     Stage 2 Lane exploration
  03-identity-system.md       identity v2 standards (current)
  fonts/                      Saira, Inter, Manrope + licences (SIL OFL 1.1)
  src/
    rr2.py                    v2 geometry: RR, 12-point ratcheting wrench, peaks, arc, true offsets (skia)
    build_v2.py               v2 logos, promo chrome, tokens, icons, graphics
    boards_v2.py, render_v2.js  v2 boards, PNG exports, size tests, PDF
    wordmark.py               font outlining (set_text) + custom-glyph override
    icons.py                  17 service icons
    geometry.py, build_stage2/3.py, boards*.py, render*.js, site_assets.py   Lane (archive + current site)
  identity/                   v2 output
    logo/svg/                 every flat lockup in dark / light / black / white
    logo/promo/               chrome promotional SVG
    logo/png/                 transparent PNG exports, chrome PNGs, size-test tiles
    logo/diagrams/            construction
    icons/, graphics/, tokens/, boards/
    ride-rescue-identity-v2.pdf
  archive/lane-v1/            previous identity + its standards doc
  exploration/stage-2/        Stage 2 concept package
```

## Rebuild

```bash
pip install skia-pathops skia-python fonttools brotli   # skia-python needs libEGL (apt-get install libegl1)
python brand/src/build_v2.py && python brand/src/boards_v2.py && node brand/src/render_v2.js
```

Change a number in `src/rr2.py` (stroke, bowl, slant, road-line run, `WRENCH` angle and proportions, knock-out gaps) and rebuild. Every SVG, PNG, board and the PDF regenerates from the same source.
