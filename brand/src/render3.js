// Render Stage 3 PNG exports, boards and PDF.
//   node brand/src/render3.js      (after python brand/src/build_stage3.py && python brand/src/boards3.py)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ID = path.resolve(__dirname, '..', 'archive', 'lane-v1', 'identity');
const SVG = path.join(ID, 'logo', 'svg');
const PNG = path.join(ID, 'logo', 'png');
fs.mkdirSync(PNG, { recursive: true });

function viewBox(svg) {
  const m = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);
  return { w: parseFloat(m[3]), h: parseFloat(m[4]) };
}

async function render(page, svgPath, w, h, out, bg) {
  const svg = fs.readFileSync(svgPath, 'utf8');
  await page.setViewportSize({ width: w, height: h });
  const b64 = Buffer.from(svg).toString('base64');
  await page.setContent(`<html><body style="margin:0;background:${bg || 'transparent'}"><img src="data:image/svg+xml;base64,${b64}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
  await page.waitForFunction(() => document.images[0].complete);
  await page.screenshot({ path: out, omitBackground: !bg, clip: { x: 0, y: 0, width: w, height: h } });
}

async function renderTile(page, svgPath, size, fillRatio, out, bg) {
  // mark centred on a square background (favicons / app-tile previews)
  const svg = fs.readFileSync(svgPath, 'utf8');
  const { w, h } = viewBox(svg);
  const mw = size * fillRatio, mh = (mw * h) / w;
  await page.setViewportSize({ width: size, height: size });
  const b64 = Buffer.from(svg).toString('base64');
  await page.setContent(`<html><body style="margin:0;width:${size}px;height:${size}px;background:${bg};display:flex;align-items:center;justify-content:center"><img src="data:image/svg+xml;base64,${b64}" style="width:${mw}px;height:${mh}px"></body></html>`);
  await page.waitForFunction(() => document.images[0].complete);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: size, height: size } });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });

  // transparent PNG exports: lockups at 1200 px wide, monograms at 1024 px wide
  for (const f of fs.readdirSync(SVG).filter((x) => x.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(SVG, f), 'utf8');
    const { w, h } = viewBox(svg);
    const W = f.startsWith('rr-monogram') ? 1024 : 1200;
    await render(page, path.join(SVG, f), W, Math.round((W * h) / w), path.join(PNG, f.replace('.svg', '.png')));
  }
  // small-size comparison tiles used on the rules board
  for (const [name, f] of [['rr-monogram-lime-on-navy', 'rr-monogram-lime.svg'], ['rr-monogram-small-lime-on-navy', 'rr-monogram-small-lime.svg']]) {
    for (const s of [16, 24, 32]) await renderTile(page, path.join(SVG, f), s, 0.84, path.join(PNG, `${name}-${s}.png`), '#14283D');
  }

  // boards
  const BO = path.join(ID, 'boards');
  const bp = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  const boards = fs.readdirSync(BO).filter((f) => f.endsWith('.html')).sort();
  for (const f of boards) {
    await bp.goto('file://' + path.join(BO, f));
    await bp.evaluate(() => document.fonts.ready);
    await bp.waitForTimeout(150);
    await bp.screenshot({ path: path.join(BO, f.replace('.html', '.png')), fullPage: true });
  }
  const pdf = await browser.newPage();
  const imgs = boards.map((f) => `<img src="file://${path.join(BO, f.replace('.html', '.png'))}" style="width:100%;display:block;page-break-after:always">`).join('');
  await pdf.setContent(`<html><body style="margin:0">${imgs}</body></html>`);
  await pdf.waitForFunction(() => [...document.images].every((i) => i.complete));
  await pdf.pdf({ path: path.join(ID, 'ride-rescue-stage-3-identity-system.pdf'), width: '1200px', height: '2000px', printBackground: true });

  await browser.close();
  console.log('stage 3 rendered');
})();
