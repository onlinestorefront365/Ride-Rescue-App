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

## Deploy: GitHub Pages on riderescueapp.com

The `CNAME` file tells GitHub Pages to serve the site at `riderescueapp.com`. The `.nojekyll` file makes Pages serve the `assets/` folder as-is.

### 1. GitHub

1. Repo **Settings → Pages**. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`. Save.
2. Custom domain: `riderescueapp.com`. Save.
3. Recommended: your profile **Settings → Pages → Add a domain** → `riderescueapp.com`. GitHub gives you a TXT record to add (below). Verifying stops anyone else from using your domain on GitHub.
4. When the DNS check passes and the certificate is issued (minutes, up to ~24h), tick **Enforce HTTPS**.

### 2. Namecheap DNS

**Domain List → riderescueapp.com → Manage → Advanced DNS.**

Delete the parking records:
- `@` record pointing to `162.255.119.26` (may show as A Record or URL Redirect)
- `www` CNAME → `parkingpage.namecheap.com`

Add:

| Type | Host | Value |
|---|---|---|
| A Record | `@` | `185.199.108.153` |
| A Record | `@` | `185.199.109.153` |
| A Record | `@` | `185.199.110.153` |
| A Record | `@` | `185.199.111.153` |
| AAAA Record | `@` | `2606:50c0:8000::153` |
| AAAA Record | `@` | `2606:50c0:8001::153` |
| AAAA Record | `@` | `2606:50c0:8002::153` |
| AAAA Record | `@` | `2606:50c0:8003::153` |
| CNAME Record | `www` | `onlinestorefront365.github.io.` |
| TXT Record | `_github-pages-challenge-onlinestorefront365` | value GitHub shows in step 3 |

TTL: Automatic. Leave the MX and SPF (TXT `v=spf1 ...`) records alone; they run Namecheap email forwarding.

### 3. Check

- https://riderescueapp.com loads the site; https://www.riderescueapp.com redirects to it.
- Send one real booking request and confirm Formspree delivers it.
