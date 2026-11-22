// Render the website's PNG icons from assets/img/*.svg
//   node brand/src/render_site_icons.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const IMG = path.resolve(__dirname, '..', '..', 'assets', 'img');
const jobs = [
  ['favicon.svg', 32, 'favicon-32.png'],
  ['app-tile-master.svg', 180, 'apple-touch-icon.png'],
  ['app-tile-master.svg', 512, 'icon-512.png'],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const [src, size, out] of jobs) {
    const b64 = fs.readFileSync(path.join(IMG, src)).toString('base64');
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(`<html><body style="margin:0"><img src="data:image/svg+xml;base64,${b64}" style="display:block;width:${size}px;height:${size}px"></body></html>`);
    await page.waitForFunction(() => document.images[0].complete);
    await page.screenshot({ path: path.join(IMG, out), omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } });
  }
  // social share image (1200x630): chrome stacked logo on carbon fibre
  const promo = path.resolve(__dirname, '..', 'identity', 'logo', 'promo', 'ride-rescue-stacked-chrome.svg');
  const tileSvg = fs.readFileSync(path.join(IMG, 'carbon-fibre-tile.svg')).toString('base64');
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(`<html><body style="margin:0;width:1200px;height:630px;background:#111315 url(data:image/svg+xml;base64,${tileSvg}) 0 0/20px 20px;display:flex;align-items:center;justify-content:center"><img src="data:image/svg+xml;base64,${fs.readFileSync(promo).toString('base64')}" style="height:600px"></body></html>`);
  await page.waitForFunction(() => document.images[0].complete);
  await page.screenshot({ path: path.join(IMG, 'og-image.jpg'), type: 'jpeg', quality: 85, clip: { x: 0, y: 0, width: 1200, height: 630 } });
  await browser.close();
  console.log('site icons rendered');
})();
