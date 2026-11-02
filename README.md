# Ride Rescue

Landing page for Ride Rescue. The first service offered is FORScan diagnostics, module programming and feature configuration for Ford, Lincoln and Mazda vehicles, done remotely or on-site.

It's a static site: plain HTML, CSS and JavaScript with no build step and no dependencies.

```
index.html              Main page
assets/css/styles.css   Styles (design tokens at the top, light + dark mode)
assets/js/main.js       Mobile nav, booking form validation and submission
assets/img/favicon.svg  Logo / favicon
```

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Before launch: replace placeholders

Swap in real values for:

| Placeholder | Where |
|---|---|
| `$[XX]` | pricing cards in `index.html` |

Also review the policy claims ("No fix, no charge", "Revert on request ... at no charge") and remove any you won't guarantee.

## Business details

- Phone: (458) 205-5060 · Email: Riderescueapp@gmail.com
- Based in Tenmile, OR 97481; on-site service anywhere in Oregon
- Travel: first 15 miles free, then the IRS standard mileage rate, round trip from 97481

These appear in the on-site card, on-site pricing tier, booking section, FAQ, footer and the JSON-LD block in `<head>`.

### Booking form (Formspree)

The form posts to `https://formspree.io/f/mkjjpwzb`, set in two places: the form `action` in `index.html` and `FORM_ENDPOINT` in `assets/js/main.js`. Change both if the form is ever replaced. Submissions arrive at the email on the Formspree account. The hidden `_gotcha` field is Formspree's spam honeypot.

## Deploy to GitHub Pages

1. Repo **Settings → Pages**.
2. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The `.nojekyll` file makes Pages serve the `assets/` folder as-is.
