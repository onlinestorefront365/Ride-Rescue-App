# Ride Rescue — Brand Identity

| Stage | Status | Files |
|---|---|---|
| 1 · Creative strategy | Draft, awaiting approval | [`01-creative-strategy.md`](01-creative-strategy.md) |
| 2 · Logo development | 3 monogram concepts, B recommended | [`02-monogram-concepts.md`](02-monogram-concepts.md), [`exploration/stage-2/`](exploration/stage-2/) |
| 3 · Identity system | Not started | — |
| 4 · Digital assets | Not started | — |
| 5 · Physical applications | Not started | — |
| 6 · Final production | Not started | — |

Nothing in `exploration/` is a final production file. These are concept-stage vectors for choosing a direction.

## Folder layout

```
brand/
  01-creative-strategy.md
  02-monogram-concepts.md
  fonts/                    Manrope variable font + licence (SIL OFL 1.1)
  src/                      Generators: the editable source for every asset
    geometry.py             Monogram construction (64-unit grid, boolean-unioned paths)
    wordmark.py             RIDE RESCUE outlines from Manrope
    build_stage2.py         Writes SVG exports + manifest
    boards.py               Writes presentation board HTML
    render.js               Renders PNG size tests, boards, PDF (Playwright)
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
python brand/src/build_stage2.py
python brand/src/boards.py
node brand/src/render.js        # needs Playwright + Chromium
```

Change a number in `src/geometry.py` (stroke, bowl height, lane taper) and rebuild. Every SVG, PNG, board and the PDF regenerates from the same source.
