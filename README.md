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

Search the repo for these and swap in real values:

| Placeholder | Where |
|---|---|
| `YOUR_FORM_ID` | `index.html` (form `action`) and `assets/js/main.js` (`FORM_ENDPOINT`) |
| `[PHONE]`, `tel:+10000000000` | footer in `index.html` |
| `[EMAIL]`, `hello@example.com` | footer in `index.html` |
| `[SERVICE AREA]` | on-site card and footer in `index.html` |
| `$[XX]` | pricing cards in `index.html` |
| `*_PLACEHOLDER` | JSON-LD block in the `<head>` of `index.html` |

Also review the policy claims ("No fix, no charge", "Revert on request ... at no charge") and remove any you won't guarantee.

### Booking form setup (Formspree)

1. Create a free form at https://formspree.io and copy its ID (the part after `/f/`).
2. Replace `YOUR_FORM_ID` in both places listed above.
3. Submissions arrive by email. The hidden `_gotcha` field is Formspree's spam honeypot.

Any service that accepts a standard form POST works (Netlify Forms, Basin, Getform); update the endpoint to match.

## Deploy to GitHub Pages

1. Repo **Settings → Pages**.
2. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
3. The `.nojekyll` file makes Pages serve the `assets/` folder as-is.
