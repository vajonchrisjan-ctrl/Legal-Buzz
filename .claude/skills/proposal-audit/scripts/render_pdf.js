// Render an addendum HTML to an A4 PDF and check every .page fits on one sheet.
// Usage: node render_pdf.js <in.html> <out.pdf>
//   (run with: node render_pdf.js ... after `export NODE_PATH=$(npm root -g)`, or pass
//    PLAYWRIGHT=$(npm root -g)/playwright). Chromium is preinstalled; never `playwright install`.
const pw = require(process.env.PLAYWRIGHT || 'playwright');
const path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const b = await pw.chromium.launch(); const p = await b.newPage();
  await p.emulateMedia({ media: 'print' });
  await p.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const fit = await p.$$eval('section.page', ss => ss.map((s, i) => {
    const t = s.getBoundingClientRect().top; let m = 0;
    for (const c of s.children) { if (c.matches('.foot,.cover-note')) continue; m = Math.max(m, c.getBoundingClientRect().bottom - t); }
    const f = s.querySelector('.foot,.cover-note'); const lim = f ? f.getBoundingClientRect().top - t : s.clientHeight;
    return { page: i + 1, contentBottom: Math.round(m), limit: Math.round(lim), overflow: m > lim };
  }));
  console.table(fit);
  if (fit.some(x => x.overflow)) console.log('OVERFLOW: trim copy or spacing on the flagged pages, then re-run.');
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log('wrote', out); await b.close();
})();
