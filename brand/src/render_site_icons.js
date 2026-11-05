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
  await browser.close();
  console.log('site icons rendered');
})();
