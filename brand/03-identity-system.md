# Ride Rescue — Stage 3: Identity System

Approved direction: **B · Lane**. Everything here is generated from `brand/src/` and lives in `brand/identity/`. Boards: `identity/boards/*.png`, or all six pages in `identity/ride-rescue-stage-3-identity-system.pdf`.

## Decisions log

| Decision | Status |
|---|---|
| Monogram direction: Lane | **Approved** |
| Re-skin riderescueapp.com in the new identity | **Approved, done in this stage** |
| Positioning: identity built for the roadside platform; the site only claims current services | Assumed (Stage 1 recommendation) — say if you want otherwise |
| Cool Gray 600 `#66717D` added for text on light | Assumed (needed for the site's accessible body copy) |
| Alert red `#B42318` / `#FF8A7A`, errors only, not a brand colour | **Needs approval**: any interface needs an error colour, and none of the brief's six can do the job accessibly |
| Wordmark R's rebuilt from monogram geometry | Made in this stage (see "Wordmark" below) |
| 3D promotional logo | Deferred to Stage 5, derived from the flat master |

---

## 1. Logo

### The system unit

**X = the monogram's stroke** (12 units when the mark is 64 units tall, so X = mark height ÷ 5.33). Every logo measurement below is in X.

### Monogram

- One compound path: 3 contours (1 outer, 2 counters). No strokes, no overlaps, no transforms.
- 64-unit cap height, 12-unit stroke, 38-unit bowls built as true semicircles.
- The stems lean apart from −1.2 units at the cap line to 9 units at the baseline, so they fuse for the top 7.5 units. The road (lane) is the negative space between them.
- **Optical overshoot:** none is needed. The bowls meet the cap line as straight bars, not curves, so there is no curve-versus-flat size illusion to correct.

### Small-size cut (16–31 px)

At 16 px the master's road disappears and its counters close. The small-size cut has a stroke of 10.5, bowls of 40, and a road 26 units wide at the baseline. The stems meet at the cap line instead of fusing. Use it **only** below 32 px: favicons, browser tabs, 16–24 px UI. Never use it as a substitute for the master.

### Wordmark

`RIDE RESCUE` in Manrope ExtraBold (800), tracked +60 (0.06 em) and converted to outlines. **Custom modification:** both R's are rebuilt from the monogram's own R construction (same 12/64 stem ratio, the same semicircular bowl and a 27° leg). Manrope 800's stem-to-cap ratio is 0.189 and the monogram's is 0.188, so the custom R's sit in the line without looking foreign, and the wordmark now repeats the mark.

### Lockups

| Lockup | Construction |
|---|---|
| Horizontal | Mark height H. Wordmark cap height 0.42H, vertically centred. Gap between them 2X |
| Stacked | Mark centred above. Wordmark width = 2 × mark width. Gap 1.5X |

**Clear space:** 2X on every side of every lockup and of the standalone mark.

### Minimum sizes

| Asset | Digital | Print |
|---|---|---|
| Horizontal lockup | 180 px wide | 45 mm wide |
| Stacked lockup | 100 px wide | 25 mm wide |
| Monogram, master | 32 px tall | 8 mm tall |
| Monogram, small-size cut | 16–31 px | 5–8 mm (embroidery 10 mm minimum) |
| Wordmark alone | 100 px wide | 25 mm wide |

The horizontal lockup's minimum is set by its monogram reaching 32 px. Below 180 px wide, switch to the stacked lockup or the monogram.

### Variations (brief section 4)

| # | Variation | File(s) in `identity/logo/svg/` |
|---|---|---|
| 1 | Primary horizontal | `ride-rescue-horizontal-dark.svg` (on navy) and `-navy.svg` (on light) |
| 2 | Primary stacked | `ride-rescue-stacked-{dark,navy,…}.svg` |
| 3 | Standalone monogram | `rr-monogram-{navy,lime,white,black}.svg` |
| 4 | Standalone wordmark | `ride-rescue-wordmark-{navy,white,black,lime}.svg` |
| 5 | Light-background | `*-navy.svg`. **Same artwork as #9**: lime can't sit on light backgrounds, so the light version is all navy by design |
| 6 | Dark-background | `*-dark.svg`: lime mark, Soft White wordmark |
| 7 | One-colour black | `*-black.svg` |
| 8 | One-colour white | `*-white.svg` |
| 9 | Monochrome navy | `*-navy.svg` |
| 10 | Monochrome lime | `*-lime.svg`, on navy or graphite only |
| 11 | Simplified small-size | `rr-monogram-small-*.svg` |
| 12 | Promotional 3D | Stage 5 |

PNG exports with transparent backgrounds are in `identity/logo/png/`: lockups at 1200 px wide and monograms at 1024 px.

### Incorrect use

Never:
- stretch, squash, rotate or skew the logo;
- put lime on a light background;
- recolour it outside the palette;
- add shadows, bevels, glows, gradients or outlines;
- re-set the wordmark in a live font (the R's are custom);
- place anything inside the clear space;
- use the small-size cut above 32 px.

---

## 2. Colour

Tokens: `identity/tokens/tokens.css` (CSS custom properties) and `tokens.json`.

| Token | HEX | Role |
|---|---|---|
| `--rr-navy` | `#14283D` | Primary brand colour, text on light |
| `--rr-lime` | `#B9E532` | Mark on dark, primary action fill, signals |
| `--rr-soft-white` | `#F5F6F2` | Light background, text on navy |
| `--rr-graphite` | `#252A30` | Secondary dark neutral |
| `--rr-cool-gray` | `#87929D` | Muted text **on navy**, borders |
| `--rr-gray-600` | `#66717D` | Muted text on light (4.58:1) |
| `--rr-amber` | `#D99B67` | Optional premium accent: tiers, annotations |

**Tints**, for interface states only and all mixed from core colours:

| Token | HEX | Use |
|---|---|---|
| `navy-deep` | `#0D1A28` | Dark-mode page, footer |
| `navy-raised` | `#24374B` | Cards on navy, hero lane graphic |
| `navy-line` | `#3E4F60` | Borders on navy |
| `navy-tint` | `#ECEEEF` | Alternate light section |
| `lime-hover` | `#A5CE33` | Button hover and pressed states |
| `lime-tint` | `#F0F9D2` | Selected state behind navy text |

**Functional:** `alert` `#B42318` on light (6.06:1) and `alert-dark` `#FF8A7A` on navy (6.55:1). Errors only.

**Action rule:** the primary button is a lime fill with a navy label (10.2:1) on every background. Secondary buttons are outlined in the text colour. Links, ticks and rules are navy on light and lime on dark.

---

## 3. Typography

| Role | Face | Size / line (desktop) | Tracking |
|---|---|---|---|
| Display | Manrope 800 | 48 / 52 (mobile 36) | −0.01 em |
| H1 | Manrope 800 | 36 / 40 (mobile 28) | −0.01 em |
| H2 | Manrope 800 | 28 / 34 | −0.01 em |
| H3 | Manrope 700 | 20 / 26 | 0 |
| Overline | Manrope 800, caps | 12 / 16 | +0.12 em |
| Body | Inter 400 | 16 / 26 | 0 |
| UI label | Inter 600 | 14 / 20 | 0 |
| Numbers, prices, ETAs | Inter 700, `font-feature-settings: "tnum"` | 20 / 24 | 0 |

Both faces are SIL OFL 1.1. The website self-hosts Latin-subset variable WOFF2 files: `assets/fonts/manrope-latin.woff2` (24 KB) and `inter-latin.woff2` (66 KB). Licences ship alongside them.

---

## 4. Iconography

There are 17 icons: the brief's 12 roadside services, plus 5 for current Ride Rescue work (diagnostics, module programming, key programming, feature configuration, service procedures).

- 24-unit grid with a 2-unit live-area padding. 2-unit stroke, round caps and joins, 2-unit corner radius.
- Vehicles face right. Wheels are r2 on y17. Badges sit inside the live area.
- Navy on light; lime or Soft White on navy; never lime on light.
- Sizes: 16, 20, 24, 32 or 48 px. Scale the whole icon; never change the stroke.
- Always pair an icon with a text label in the interface.

Files: `identity/icons/svg/*.svg` (they use `currentColor`) and `identity/icons/sprite.svg` (`<use href="sprite.svg#rr-towing">`).

---

## 5. Graphic language

| Element | File | Rule |
|---|---|---|
| Lane wedge | `graphics/lane-wedge-{raised,lime,navy}.svg` | The logo's negative space, extracted. One per layout, large and cropped. Navy Raised on navy; lime only at small sizes. Never rotated |
| Road-marking pattern | `graphics/pattern-road-tile.svg` | Staggered dashes on the 12-unit rhythm. Navy Raised on navy only. Use for loading screens, banners and card backs |
| Lane divider | `graphics/lane-divider-{navy,lime}.svg` | Tapered rule. The site uses it before every overline |
| Direction wedge | `graphics/direction-wedge-{navy,lime}.svg` | "Next step" cue, in place of generic arrows |
| Cut-corner frame | `graphics/cut-corner-frame.svg` | Top-right corner clipped at 45°, cut = 2X. One per view |

There are no checker, chevron or racing-stripe patterns anywhere in the system (see the emergency-vehicle note in Stage 1).

---

## 6. What changed on riderescueapp.com

- New lockup in the header and footer. Favicon uses the small-size cut, and there are Apple touch and social icons.
- All colours now come from the brand tokens, in light mode and OS dark mode. Header, hero, CTA band and footer are always dark.
- Manrope for headings and labels, Inter for body text and forms, with tabular figures on prices.
- Service cards carry the new icons.
- The hero has a Navy Raised lane wedge, overlines have lane dividers, and the CTA band has the road pattern.

## Next: Stage 4 (digital assets)

- App Store icon (1024, full-bleed, no transparency) and Google Play icon (512).
- Android adaptive icon layers (foreground mark inside the 66 dp safe zone).
- Social profile, cover and banner art; loading and splash screens; the full UI token set for the app.
