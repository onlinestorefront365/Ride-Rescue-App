# Ride Rescue — Stage 1: Creative Strategy

Status: positioning, personality and principles still apply. **Sections 3 (colour) and 4 (typography), and the logo direction, are superseded by identity v2**: see `03-identity-system.md`.

## 1. Positioning

**Ride Rescue is an assistance platform with a dependable physical service network, not a tow company with an app.**

The customer usually meets the brand on a bad day: a dead battery, a no-start after a repair, a dashboard full of warning lights. In that moment the identity has one job: make them feel that someone competent is in control. That means clarity first, then personality.

| The category default | Ride Rescue |
|---|---|
| Red, safety yellow, black, hazard chevrons | Midnight navy with one electric-lime signal |
| Tow hooks, wrenches, shields, lightning bolts | A typographic monogram with one idea in its negative space |
| Racing italics, outlines, chrome | Upright geometric sans, flat colour |
| Shouting urgency | Calm, fast competence |

**Brand line (working):** *Help that knows where it's going.*

## 2. Personality → design rules

| Trait | Not | Design rule it produces |
|---|---|---|
| Confident | Arrogant | Heavy, upright letterforms; no exclamation-mark energy, no italics |
| Modern | Trendy | Geometry from circles and straight lines; no gradients or glass effects in master art |
| Professional | Impersonal | Navy carries the brand; lime is used sparingly, like a signal light |
| Approachable | Childish | Rounded bowls, generous counters; no mascots, no cartoon vehicles |
| Responsive | Frantic | One accent colour, lots of space; motion motifs point forward, never zig-zag |
| Strong | Intimidating | Wide, stable silhouettes; no aggressive spikes or angled "attack" shapes |

## 3. Colour system

### Core palette

The brief's six colours are kept. One refinement is added (Cool Gray 600) for accessibility, explained below.

| Colour | HEX | RGB | CMYK (conversion, see note) | Role |
|---|---|---|---|---|
| Midnight Navy | `#14283D` | 20 40 61 | 67 34 0 76 | Primary brand colour, dark backgrounds, text on light |
| Electric Lime | `#B9E532` | 185 229 50 | 19 0 78 10 | Recognition and action: the mark on dark, primary buttons, key highlights |
| Soft White | `#F5F6F2` | 245 246 242 | 0 0 2 4 | Primary light background, text on navy |
| Graphite | `#252A30` | 37 42 48 | 23 13 0 81 | Secondary dark neutral (UI surfaces, uniforms) |
| Cool Gray | `#87929D` | 135 146 157 | 14 7 0 38 | Dividers, borders, disabled states, muted text **on navy only** |
| Champagne Amber | `#D99B67` | 217 155 103 | 0 29 53 15 | Optional premium accent: membership tiers, annotations. Never next to lime as a co-accent |
| **Cool Gray 600** *(proposed)* | `#66717D` | 102 113 125 | 18 10 0 51 | Secondary text on light backgrounds |

**CMYK note:** these are straight mathematical conversions, which is what the brief asked for. They are not press-ready. Final print values must come from a proof against the printer's profile (for example GRACoL coated or SWOP uncoated), with Pantone and vinyl matches chosen in Stage 6. Electric Lime sits near the edge of the CMYK gamut and will print duller than it looks on screen. For vehicles and uniforms, plan on a spot colour or a stock lime vinyl, not process CMYK.

### Contrast (WCAG 2.x)

| Foreground on background | Ratio | Use |
|---|---|---|
| Soft White on Navy | **13.81** | All text sizes |
| Navy on Soft White | **13.81** | All text sizes |
| Lime on Navy | **10.22** | All text sizes, icons, the mark |
| Navy on Lime | **10.22** | Button labels, badges |
| Lime on Graphite | **9.86** | All text sizes |
| Amber on Navy | **6.31** | Text OK; keep to accents |
| Cool Gray on Navy | **4.73** | Secondary text on dark: passes AA |
| Cool Gray on Soft White | 2.92 | **Fails** for text → use Cool Gray 600 (4.58) |
| Amber on Soft White | 2.19 | **Fails**: decorative only on light |
| Lime on Soft White | 1.35 | **Fails badly**: never lime text, lines or icons on light |

**Rule that follows:** on light backgrounds, lime may only appear as a solid fill block carrying navy content, such as a lime button with a navy label. The mark on light backgrounds is always navy.

### Distribution

The 60 / 20 / 15 / 5 split is a guide for brand-led surfaces (app, website hero, vehicles), not for every asset. Documents and receipts flip it: mostly Soft White, navy text, and lime only on the single most important action or figure.

## 4. Typography direction

| Role | Typeface | Weights | Tracking | Licence |
|---|---|---|---|---|
| Wordmark | Manrope, outlined | 800 | +60 (0.06 em), all caps | SIL OFL 1.1 |
| Headings, display | Manrope | 700–800 | −10 (−0.01 em) | SIL OFL 1.1 |
| Labels, overlines | Manrope | 700 | +120, all caps | SIL OFL 1.1 |
| Body, UI | Inter | 400, 500, 600 | 0 | SIL OFL 1.1 |
| Numbers, prices, ETAs | Inter, tabular figures (`font-feature-settings: "tnum"`) | 600–700 | 0 | SIL OFL 1.1 |

Two families, no more. Manrope gives the brand its geometric, confident voice. Inter handles dense mobile UI and numbers, which must line up in receipts and ETAs. Both are free for commercial use, apps, web embedding and print under the SIL Open Font License. The only restriction is selling the font files themselves.

Rejected options: **Space Grotesk**, whose serifed I and quirky details feel too start-up for a trust brand; and **Sora**, which is a strong alternative but too wide for long vehicle-side runs. Sora remains the fallback if Manrope is rejected.

## 5. Visual principles

1. **One idea per mark.** The monogram gets one concept in its negative space, and nothing else is layered on.
2. **Flat master, decorated derivatives.** The flat vector logo is the only authority. The 3D logo, mockups and textures are derived from it and never fed back into it.
3. **Build on the 64 / 12 grid.** Monogram cap height 64 units, master stroke 12 units, bowl 38 units. Icons, patterns and dividers inherit the same 12-unit rhythm and the same corner logic.
4. **Lime is a signal, not a paint.** If everything is lime, nothing is.
5. **Legible at the worst moment.** Every asset is checked at the smallest size and lowest contrast it will realistically meet: a phone in sunlight, a van passing at 40 mph.

## 6. Competitive position

Roadside and auto-service brands cluster around red, yellow, orange and black, plus tow-hook, wrench and shield symbols. Navy with lime is uncommon in the category, so it is ownable. It also avoids the emergency-red shorthand that can make a service look like a hazard rather than a help.

## 7. Production note: emergency-vehicle look-alike risk

Navy or blue with fluorescent yellow-green is the colour pairing of the UK and European "Battenburg" police and ambulance livery. It is distinctive for a reason. Stage 5 vehicle graphics must avoid checkerboard and chevron patterns, the word "Emergency", and anything else that reads as an official vehicle. Use lime as solid brand panels only. Before any vehicle graphics or warning lights are specified, check Oregon's rules on vehicle markings and lighting. I have not verified Oregon-specific restrictions.

## 8. Decisions needed before Stage 3

1. **Positioning scope.** This brief describes a roadside-assistance platform (towing, jump-starts, fuel, lockouts). The business currently live on riderescueapp.com is FORScan diagnostics and programming in Tenmile, OR. **Recommendation:** build the identity for the platform vision, but keep the website's service claims to what you actually offer today. The service icon set (Stage 3) will include diagnostics and programming alongside the roadside icons.
2. **Monogram direction.** Approve B (Lane), or pick A or C. See `02-monogram-concepts.md`.
3. **Website re-skin.** The live site uses slate and safety orange. Adopting this identity means re-skinning it in Stage 4. **Recommendation:** yes, and swap the favicon at the same time.
4. **Cool Gray 600 (`#66717D`).** Approve as the one added colour, for text on light backgrounds only.
5. **Trademark check.** Search "Ride Rescue" in the USPTO trademark database (and the Oregon business registry) before spending on vehicles, uniforms or signage. I have not run that search, and I can't confirm the name is clear.
