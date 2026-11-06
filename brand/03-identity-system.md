# Ride Rescue — Identity System v2

Direction: your chrome, gear and mountain reference image, used as the **visual direction rather than the logo itself**, and rebuilt as a flat vector system. Everything is generated from `brand/src/` (`rr2.py`, `build_v2.py`) into `brand/identity/`.

Boards: `identity/boards/*.png`, or all six pages in `identity/ride-rescue-identity-v2.pdf`.

The previous Lane / navy-lime system is archived in `archive/lane-v1/`. **The live website still uses it** until this system is approved; then the site is re-skinned and gains a repairs section.

## Decisions log

| Decision | Status |
|---|---|
| Reference image = visual direction only; flat vector master is the authority | **Agreed** |
| The RR is the identity; gear and mountains are supporting symbolism | **Agreed** |
| Palette: Electric Blue `#087FFF`, Steel Silver `#C3C9D0`, Carbon Black `#111315`, White | **Agreed** |
| Tagline "Mobile Diagnostics • Programming • Repairs" (repairs added to services) | **Agreed** |
| Identity first, website after approval | **Agreed** |
| Saira Italic (wdth 112, wght 800) for display; Inter for body | Chosen this stage: closest open-licence match to the reference lettering |
| RR construction: "Drive" (first R's leg runs on as a road line past the second R) | Chosen this stage. Pair and Interlock rejected: generic, and the first R read as "F" |
| Action Blue `#0973E5` for buttons/links on light | **Needs approval**: white on Electric Blue is 3.83:1 and fails for button text |
| Steel 600 `#73777C` for the gear on light backgrounds and for muted text | **Needs approval**: Steel Silver on white is 1.67:1 |
| Wrench from the reference dropped | Simplification: gear plus RR already say "mechanic"; a wrench would add clutter at small sizes |

---

## 1. Logo levels

| Level | What it is | Files (`identity/logo/svg/`) | Use |
|---|---|---|---|
| **Primary** | Emblem (RR + gear + Oregon peaks + blue arc) with the wordmark and tagline | `ride-rescue-stacked-*.svg`, `ride-rescue-horizontal-*.svg`, `emblem-*.svg` | Website hero, signage, vehicle side, print |
| **Secondary** | RR inside the gear, with no mountain or arc | `rr-gear-*.svg`, `ride-rescue-horizontal-compact-*.svg` | Headers, uniforms, stickers, social avatars |
| **Micro** | The RR alone | `rr-micro-{white,carbon,blue,silver,black}.svg` | App icon, favicon, embroidery on caps, anywhere under 48 px |
| **Promotional** | Chrome-rendered version of the primary | `logo/promo/*-chrome.svg` and PNG | Banners, ads, presentations, video. Never the master |

Colourways for every flat lockup: `dark` (full colour on Carbon), `light` (full colour on white), `black` and `white` (one colour).

### The RR (micro mark)

- Each R is drawn upright on a 64-unit grid from rounded-square parts. **The stroke, X, is 16 units.** The bowl is 46 units, with 16-unit outer and 4-unit inner corner radii. The R is then slanted **12°**, Saira Italic's own angle, so mark and wordmark share one slant.
- The first R's leg runs on as a tapered **road line** under the second R and past it. This is the ownable detail; nothing else in the category has it.
- One compound path with 4 contours.
- It reads at 16 px. Below 24 px it is the only version to use.

### Gear, peaks and arc

- **Gear:** 9 teeth with a ring about 1X thick. It is knocked out around the RR with a 5-unit gap (true offset, round joins), so the RR always sits in front.
- **Peaks:** a two-summit ridge with snow caps separated by a jagged 3.2-unit gap. Because the caps are separate pieces, they still read in one colour, vinyl and embroidery.
- **Arc:** a tapered crescent in Electric Blue, sweeping from outside the gear at lower left to the upper right. It is knocked out of the gear with a 3-unit gap.
- **Secondary mark:** with no peaks, the RR sits optically centred in the gear. With the peaks (primary), it sits lower so the summits fill the top.

### Wordmark

`RIDE RESCUE` in Saira Italic, width 112 and weight 800, tracked +20, converted to outlines. **Custom modification:** every R is the monogram's R, not Saira's. In colour, RIDE is Steel Silver on dark (Carbon on light) and RESCUE is Electric Blue. A tapered road line separates the wordmark from the tagline (Saira Italic 600, tracked +160).

### Clear space

Clear space is 1X around every lockup, measured at the size the RR appears in it, and 2X around the micro mark on its own.

### Minimum sizes (checked at actual pixels on the rules board)

| Asset | Digital | Print | Below that, use |
|---|---|---|---|
| Micro mark | 16 px | 5 mm tall | — |
| Secondary (RR in gear) | 48 px | 12 mm | Micro mark |
| Primary emblem | 96 px | 25 mm | Secondary |
| Stacked lockup | 200 px wide | 50 mm | Secondary + wordmark |
| Horizontal lockup | 280 px wide | 70 mm | Compact horizontal |
| Compact horizontal | 180 px wide | 45 mm | Micro mark |

### Incorrect use

Never:
- show the gear without the RR;
- stretch, squash or skew any version;
- recolour outside the palette;
- use the chrome version for one-colour, vinyl, embroidery, the app icon or the favicon;
- set Electric Blue body text on white;
- rebuild the RR or the wordmark in a live font.

### Promotional chrome

The chrome version is generated from the same paths, with gradient fills, specular bevel lighting, a drop shadow and a glow on the arc. It is a derivative: whenever it and the flat master disagree, the flat master wins.

---

## 2. Colour

Tokens: `identity/tokens/tokens.css` and `tokens.json`.

| Colour | HEX | RGB | CMYK (conversion) | Role |
|---|---|---|---|---|
| Electric Blue | `#087FFF` | 8 127 255 | 97 50 0 0 | The signal: arc, RESCUE, active states, ~5% of a surface |
| Steel Silver | `#C3C9D0` | 195 201 208 | 6 3 0 18 | Gear, peaks, RIDE on dark, secondary text on dark |
| Carbon Black | `#111315` | 17 19 21 | 19 10 0 92 | Primary background, text on light |
| White | `#FFFFFF` | 255 255 255 | 0 0 0 0 | RR on dark, light backgrounds |

**Derived values** (each mixed from the core four, proposed):

| Token | HEX | Use |
|---|---|---|
| `action-blue` | `#0973E5` | Buttons and links on light. White label 4.57:1 |
| `steel-600` | `#73777C` | Gear on light backgrounds, muted text on white (4.51:1) |
| `carbon-raised` | `#1F2123` | Cards and surfaces on dark |
| `carbon-line` | `#37393A` | Borders on dark |
| `steel-tint` | `#F0F2F3` | Alternate light section |
| `blue-tint` | `#E6F2FF` | Selected background behind carbon text |

**Functional:** `alert` `#C4320A` and `alert-dark` `#FF8A66`, for errors only.

| Contrast | Ratio | Rule |
|---|---|---|
| White on Carbon | 18.62 | All text |
| Steel Silver on Carbon | 11.16 | All text |
| Electric Blue on Carbon | 4.87 | All text |
| White on Electric Blue | 3.83 | Large text only, so buttons on light use Action Blue |
| Electric Blue on white | 3.83 | Large text and logo only |
| Steel Silver on white | 1.67 | Never for text, so use Steel 600 |

**Print note:** Electric Blue is outside the CMYK gamut and prints duller than on screen. Choose a Pantone or vinyl match from a physical swatch before ordering vehicle graphics or signage.

---

## 3. Typography

| Role | Face | Size / line (desktop) | Tracking |
|---|---|---|---|
| Display | Saira Italic 800, wdth 112 | 52 / 54 | 0 |
| H1 | Saira Italic 800, wdth 112 | 36 / 40 | 0 |
| H2 | Saira Italic 700, wdth 112 | 28 / 32 | 0 |
| Overline, tagline | Saira Italic 600, caps | 13 / 16 | +0.16 em |
| H3 | Inter 700 | 20 / 26 | 0 |
| Body | Inter 400 | 16 / 26 | 0 |
| UI label | Inter 600 | 14 / 20 | 0 |
| Numbers | Inter 700, tabular figures | 20 / 24 | 0 |

Both families are SIL OFL 1.1 and free for commercial print, web, app and vehicle use. Source files are in `brand/fonts/`. The website build will ship Latin-subset WOFF2 files, as before.

---

## 4. Icons and graphic language

- **Icons:** the 17 service icons keep their drawing (24-unit grid, 2-unit stroke). They are recoloured: Carbon on light, Steel Silver on dark, Electric Blue only for the active or selected state.
- **Road line** (`graphics/road-line-*.svg`): the RR's road line as a tapered rule, used under headings and between the wordmark and tagline.
- **Arc** (`graphics/swoosh-blue.svg`): one per layout, as a hero accent.
- **Ridge band** (`graphics/ridge-band-*.svg`): the peaks run out to a horizon, used along the bottom of hero sections in Carbon Raised.
- **Gear quarter** (`graphics/gear-quarter-*.svg`): for section corners, in Carbon Raised on Carbon only.
- None of these is ever used as a logo. The gear never appears without the RR in a logo context.

---

## Next

1. You approve the system, plus Action Blue and Steel 600.
2. **Website:** re-skin to Carbon, Steel and Electric Blue with the new lockups and favicon; add the repairs service section; update the tagline and metadata.
3. **Stage 4:** App Store and Google Play icons (micro mark on Carbon with an Electric Blue accent), social avatar and banners, splash screen.
