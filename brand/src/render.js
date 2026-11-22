// Render PNG size tests and presentation boards for Stage 2.
//   node brand/src/render.js
// Requires Playwright with Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = path.resolve(__dirname, '..', 'exploration', 'stage-2');
const manifest = JSON.parse(fs.readFileSync(path.join(OUT, 'manifest.json'), 'utf8'));
const PNG = path.join(OUT, 'png');
fs.mkdirSync(PNG, { recursive: true });

async function renderSvg(page, svgFile, w, h, out, transparent) {
  const svg = fs.readFileSync(svgFile, 'utf8');
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(
    `<html><body style="margin:0;background:transparent"><img src="data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}" style="display:block;width:${w}px;height:${h}px"></body></html>`
  );
  await page.waitForFunction(() => document.images[0].complete);
  await page.screenshot({ path: out, omitBackground: transparent, clip: { x: 0, y: 0, width: w, height: h } });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });

  for (const [key, c] of Object.entries(manifest.concepts)) {
    const dir = path.join(OUT, key);
    for (const s of manifest.sizes) {
      // opaque app tile
      await renderSvg(page, path.join(dir, c.files['app-tile']), s, s, path.join(PNG, `${key}-app-${s}.png`), false);
      // transparent mark, width = s
      const h = Math.round((s * c.height) / c.width);
      await renderSvg(page, path.join(dir, c.files['mark-navy']), s, h, path.join(PNG, `${key}-mark-navy-${s}.png`), true);
    }
  }

  const boards = fs.readdirSync(OUT).filter((f) => f.startsWith('board-') && f.endsWith('.html'));
  const bp = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  for (const f of boards) {
    await bp.goto('file://' + path.join(OUT, f));
    await bp.evaluate(() => document.fonts.ready);
    await bp.screenshot({ path: path.join(OUT, f.replace('.html', '.png')), fullPage: true });
  }

  // one PDF with every board, for sharing
  const pdfPage = await browser.newPage();
  const order = ['board-overview.html', 'board-a-tandem.html', 'board-b-lane.html', 'board-c-route.html'];
  const imgs = order.map((f) => `<img src="file://${path.join(OUT, f.replace('.html', '.png'))}" style="width:100%;display:block;page-break-after:always">`).join('');
  await pdfPage.setContent(`<html><body style="margin:0">${imgs}</body></html>`);
  await pdfPage.waitForFunction(() => [...document.images].every((i) => i.complete));
  await pdfPage.pdf({ path: path.join(OUT, 'ride-rescue-stage-2-monogram-concepts.pdf'), width: '1200px', height: '1800px', printBackground: true });

  await browser.close();
  console.log('rendered');
})();
