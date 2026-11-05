# Ride Rescue — Brand Identity

| Stage | Status | Files |
|---|---|---|
| 1 · Creative strategy | Approved (positioning assumed per recommendation) | [`01-creative-strategy.md`](01-creative-strategy.md) |
| 2 · Logo development | B · Lane approved | [`02-monogram-concepts.md`](02-monogram-concepts.md), [`exploration/stage-2/`](exploration/stage-2/) |
| 3 · Identity system | Done, awaiting review | [`03-identity-system.md`](03-identity-system.md), [`identity/`](identity/) |
| 4 · Digital assets | Not started | — |
| 5 · Physical applications | Not started | — |
| 6 · Final production | Not started | — |

Nothing in `exploration/` is a final production file. These are concept-stage vectors for choosing a direction. The approved system lives in `identity/`.

## Folder layout

```
brand/
  01-creative-strategy.md
  02-monogram-concepts.md
  03-identity-system.md
  fonts/                    Manrope + Inter variable fonts + licences (SIL OFL 1.1)
  src/                      Generators: the editable source for every asset
    geometry.py             Monogram construction (64-unit grid, boolean-unioned paths)
    wordmark.py             RIDE RESCUE outlines from Manrope
    build_stage2.py         Writes SVG exports + manifest
    boards.py               Writes presentation board HTML
    render.js               Renders PNG size tests, boards, PDF (Playwright)
    icons.py                Service icon family (24-unit grid)
    build_stage3.py         Logo family, icons, graphics, tokens
    boards3.py, render3.js  Stage 3 boards, PNG exports, PDF
    site_assets.py, render_site_icons.js   Copies brand assets into the website
  identity/
    logo/svg/               every logo variation (single compound paths)
    logo/png/               transparent PNG exports
    logo/diagrams/          construction + clear space
    icons/svg/, sprite.svg  17 service icons
    graphics/               lane wedge, divider, pattern, direction wedge, frame
    tokens/                 tokens.css, tokens.json
    boards/                 Stage 3 presentation boards
    ride-rescue-stage-3-identity-system.pdf
  exploration/stage-2/
    a-tandem/  b-lane/  c-route/
      *-mark-{navy,lime,white,black}.svg    single compound path, transparent
      *-lockup-{light,dark}.svg             horizontal lockup, wordmark outlined
      *-app-tile.svg                        full-bleed square app tile
      *-construction.svg                    grid + negative-space diagram
    png/                    1024 / 512 / 128 / 64 / 32 px tests (app tile + transparent mark)
    board-*.png             presentation boards
    ride-rescue-stage-2-monogram-concepts.pdf
```

## Rebuild

```bash
pip install skia-pathops fonttools
python brand/src/build_stage3.py && python brand/src/boards3.py && node brand/src/render3.js
python brand/src/site_assets.py && node brand/src/render_site_icons.js   # update the website
# Stage 2 exploration: build_stage2.py, boards.py, render.js
```

Change a number in `src/geometry.py` (stroke, bowl height, lane taper) and rebuild. Every SVG, PNG, board and the PDF regenerates from the same source.
