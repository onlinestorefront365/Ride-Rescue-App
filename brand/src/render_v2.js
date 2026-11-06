// Identity v2: PNG exports, actual-pixel size tests, boards and PDF.
//   node brand/src/render_v2.js   (after build_v2.py and boards_v2.py)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ID = path.resolve(__dirname, '..', 'identity');
const SVG = path.join(ID, 'logo', 'svg');
const PROMO = path.join(ID, 'logo', 'promo');
const PNG = path.join(ID, 'logo', 'png');
fs.mkdirSync(PNG, { recursive: true });

const vb = (svg) => { const m = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/); return { w: +m[3], h: +m[4] }; };
const b64 = (f) => fs.readFileSync(f).toString('base64');

async function shot(page, file, w, h, out, bg) {
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<html><body style="margin:0;background:${bg || 'transparent'}"><img src="data:image/svg+xml;base64,${b64(file)}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
  await page.waitForFunction(() => document.images[0].complete);
  await page.waitForTimeout(30);
  await page.screenshot({ path: out, omitBackground: !bg, clip: { x: 0, y: 0, width: w, height: h } });
}

async function tile(page, file, size, fill, out, bg) {
  const { w, h } = vb(fs.readFileSync(file, 'utf8'));
  let mw = size * fill, mh = (mw * h) / w;
  if (mh > size * fill) { mh = size * fill; mw = (mh * w) / h; }
  await page.setViewportSize({ width: size, height: size });
  await page.setContent(`<html><body style="margin:0;width:${size}px;height:${size}px;background:${bg};display:flex;align-items:center;justify-content:center"><img src="data:image/svg+xml;base64,${b64(file)}" style="width:${mw}px;height:${mh}px"></body></html>`);
  await page.waitForFunction(() => document.images[0].complete);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: size, height: size } });
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });

  for (const f of fs.readdirSync(SVG).filter((x) => x.endsWith('.svg'))) {
    const { w, h } = vb(fs.readFileSync(path.join(SVG, f), 'utf8'));
    const W = f.startsWith('rr-') || f.startsWith('emblem') ? 1024 : 1600;
    const H = Math.round((W * h) / w);
    await shot(page, path.join(SVG, f), W, H, path.join(PNG, f.replace('.svg', '.png')));
  }
  for (const f of fs.readdirSync(PROMO).filter((x) => x.endsWith('.svg'))) {
    const { w, h } = vb(fs.readFileSync(path.join(PROMO, f), 'utf8'));
    const W = 2000, H = Math.round((W * h) / w);
    await shot(page, path.join(PROMO, f), W, H, path.join(PNG, f.replace('.svg', '.png')), '#000');
  }
  for (const s of [16, 24, 32, 48]) await tile(page, path.join(SVG, 'rr-micro-white.svg'), s, 0.86, path.join(PNG, `tile-micro-${s}.png`), '#111315');
  for (const s of [48, 64, 96]) await tile(page, path.join(SVG, 'rr-wrench-dark.svg'), s, 0.94, path.join(PNG, `tile-wrench-${s}.png`), '#111315');
  for (const s of [64, 96, 128]) await tile(page, path.join(SVG, 'emblem-dark.svg'), s, 0.92, path.join(PNG, `tile-emblem-${s}.png`), '#111315');

  const BO = path.join(ID, 'boards');
  const bp = await browser.newPage({ viewport: { width: 1200, height: 800 }, deviceScaleFactor: 1 });
  const boards = fs.readdirSync(BO).filter((f) => f.endsWith('.html')).sort();
  for (const f of boards) {
    await bp.goto('file://' + path.join(BO, f));
    await bp.evaluate(() => document.fonts.ready);
    await bp.waitForTimeout(300);
    await bp.screenshot({ path: path.join(BO, f.replace('.html', '.png')), fullPage: true });
  }
  const pdf = await browser.newPage();
  const imgs = boards.map((f) => `<img src="file://${path.join(BO, f.replace('.html', '.png'))}" style="width:100%;display:block;page-break-after:always">`).join('');
  await pdf.setContent(`<html><body style="margin:0">${imgs}</body></html>`);
  await pdf.waitForFunction(() => [...document.images].every((i) => i.complete));
  await pdf.pdf({ path: path.join(ID, 'ride-rescue-identity-v2.pdf'), width: '1200px', height: '2100px', printBackground: true });
  await browser.close();
  console.log('identity v2 rendered');
})();
