// Builds the SEO baseline PDF for a client from a JSON data file.
// Usage: node build.js data/<client>.json [output/<name>.pdf]
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const dataPath = process.argv[2];
if (!dataPath) {
  console.error('Usage: node build.js data/<client>.json [output.pdf]');
  process.exit(1);
}
const d = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const slug = path.basename(dataPath, '.json');
const outPath = process.argv[3] || path.join(__dirname, 'output', `${slug}-seo-baseline.pdf`);

const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const has = (v) => v !== null && v !== undefined && v !== '';
const dash = '<span class="empty">—</span>';
const val = (v, fmt = (x) => x) => (has(v) ? esc(fmt(v)) : dash);
const fmtDate = (iso) => (iso ? new Date(iso + 'T00:00:00Z').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }) : null);
const num = (n) => Number(n).toLocaleString('en-GB');

// Lighthouse score bands: 90+ good, 50-89 needs work, under 50 poor.
const scoreBand = (s) => (s >= 90 ? 'good' : s >= 50 ? 'warn' : 'poor');

// Core Web Vitals thresholds (good / poor) as published by Google.
const VITALS = [
  { key: 'lcp_s', name: 'Largest Contentful Paint', desc: 'Main content visible', unit: 's', good: 2.5, poor: 4 },
  { key: 'cls', name: 'Cumulative Layout Shift', desc: 'Visual stability', unit: '', good: 0.1, poor: 0.25 },
  { key: 'tbt_ms', name: 'Total Blocking Time', desc: 'Responsiveness', unit: 'ms', good: 200, poor: 600 },
  { key: 'fcp_s', name: 'First Contentful Paint', desc: 'First content visible', unit: 's', good: 1.8, poor: 3 },
  { key: 'si_s', name: 'Speed Index', desc: 'How fast the page fills in', unit: 's', good: 3.4, poor: 5.8 },
];
const vitalBand = (v, t) => (v <= t.good ? 'good' : v <= t.poor ? 'warn' : 'poor');
const BAND_LABEL = { good: 'Good', warn: 'Needs work', poor: 'Poor' };
const pill = (band, label = BAND_LABEL[band]) => `<span class="pill ${band}">${esc(label)}</span>`;

function ring(score, label) {
  const r = 34, c = 2 * Math.PI * r;
  const band = has(score) ? scoreBand(score) : 'none';
  const off = has(score) ? c * (1 - score / 100) : c;
  return `<div class="ring">
    <svg viewBox="0 0 84 84" width="84" height="84">
      <circle cx="42" cy="42" r="${r}" class="ring-track"/>
      <circle cx="42" cy="42" r="${r}" class="ring-val ${band}" stroke-dasharray="${c.toFixed(2)}" stroke-dashoffset="${off.toFixed(2)}" transform="rotate(-90 42 42)"/>
      <text x="42" y="48" text-anchor="middle" class="ring-num ${band}">${has(score) ? score : '—'}</text>
    </svg>
    <div class="ring-label">${esc(label)}</div>
  </div>`;
}

function scoreRow(device, s) {
  return `<div class="score-row">
    <div class="device">${device}</div>
    ${ring(s?.performance, 'Performance')}${ring(s?.accessibility, 'Accessibility')}${ring(s?.best_practices, 'Best practices')}${ring(s?.seo, 'SEO')}
  </div>`;
}

const awaiting = (source) => `<div class="awaiting">Awaiting data${source ? ` from ${esc(source)}` : ''}. This section fills in once figures are added to the client data file.</div>`;
const blankRows = (cols, n = 5) => Array.from({ length: n }, () => `<tr>${'<td>&nbsp;</td>'.repeat(cols)}</tr>`).join('');

// Ranking position buckets, best first.
const BUCKETS = [
  { label: 'Top 3', test: (p) => p >= 1 && p <= 3 },
  { label: '4–10', test: (p) => p >= 4 && p <= 10 },
  { label: '11–20', test: (p) => p >= 11 && p <= 20 },
  { label: '21–50', test: (p) => p >= 21 && p <= 50 },
  { label: '51–100', test: (p) => p >= 51 && p <= 100 },
  { label: 'Not ranking', test: (p) => !has(p) || p > 100 },
];

function distribution(all) {
  const counts = BUCKETS.map((b) => all.filter((k) => b.test(k.position)).length);
  const max = Math.max(1, ...counts);
  const rows = BUCKETS.map((b, i) => `<div class="dist-row">
      <div class="dist-label">${b.label}</div>
      <div class="dist-track"><div class="dist-bar b${i}" style="width:${all.length ? (counts[i] / max) * 100 : 0}%"></div></div>
      <div class="dist-num">${all.length ? counts[i] : '—'}</div>
    </div>`).join('');
  return `<div class="dist">${rows}</div>`;
}

const posCell = (p) => {
  if (!has(p)) return '<td class="num"><span class="pos none">—</span></td>';
  const cls = p <= 3 ? 'top3' : p <= 10 ? 'top10' : p <= 20 ? 'top20' : 'low';
  return `<td class="num"><span class="pos ${cls}">${p}</span></td>`;
};

function kwTable(title, rows, source) {
  const body = rows.length
    ? [...rows].sort((a, b) => (a.position ?? 999) - (b.position ?? 999)).map((k) => `<tr>
        <td>${esc(k.keyword)}</td>
        <td class="num">${val(k.volume, num)}</td>
        ${posCell(k.position)}
        <td class="url">${val(k.url && k.url.replace(/^https?:\/\/[^/]+/, '') || null)}</td>
      </tr>`).join('')
    : blankRows(4);
  return `<h3>${title}</h3>
    ${rows.length ? '' : awaiting(source)}
    <table class="data">
      <thead><tr><th>Keyword</th><th class="num">Monthly searches</th><th class="num">Position</th><th>Ranking page</th></tr></thead>
      <tbody>${body}</tbody>
    </table>`;
}

function render() {
  const c = d.client, sh = d.site_health, rk = d.rankings, bl = d.backlinks;
  const allKw = [...(rk.location || []), ...(rk.service || [])];
  const ranked = allKw.filter((k) => has(k.position) && k.position <= 100);
  const top10 = allKw.filter((k) => has(k.position) && k.position <= 10).length;

  const snapshot = [
    { label: 'Mobile performance', value: sh.mobile?.performance, sub: 'out of 100' },
    { label: 'Main content load (mobile)', value: has(sh.mobile?.lcp_s) ? `${sh.mobile.lcp_s}s` : null, sub: 'target under 2.5s' },
    { label: 'Keywords in top 10', value: allKw.length ? `${top10}/${allKw.length}` : null, sub: 'location and service' },
    { label: 'Referring domains', value: bl.metrics?.['Referring domains'], sub: 'unique linking sites' },
  ];

  const vitalsRows = VITALS.map((t) => {
    const cell = (s) => {
      const v = s?.[t.key];
      return has(v) ? `<td class="num">${v}${t.unit}</td><td>${pill(vitalBand(v, t))}</td>` : `<td class="num">${dash}</td><td></td>`;
    };
    return `<tr><td><strong>${t.name}</strong><div class="muted">${t.desc} · good ≤ ${t.good}${t.unit}</div></td>${cell(sh.mobile)}${cell(sh.desktop)}</tr>`;
  }).join('');

  const issues = (sh.issues || []).map((i) => `<tr>
      <td>${pill(i.priority === 'High' ? 'poor' : i.priority === 'Medium' ? 'warn' : 'low', i.priority)}</td>
      <td class="area">${esc(i.area)}</td><td>${esc(i.issue)}</td></tr>`).join('');

  const platform = Object.entries(sh.platform || {}).map(([k, v]) => `<div class="kv"><span>${esc(k)}</span><strong>${esc(v)}</strong></div>`);

  const metrics = Object.entries(bl.metrics || {}).map(([k, v]) => `<div class="tile"><div class="tile-num">${val(v, (x) => (typeof x === 'number' ? num(x) : x))}</div><div class="tile-label">${esc(k)}</div></div>`).join('');
  const blHas = Object.values(bl.metrics || {}).some(has) || (bl.top_referring_domains || []).length;

  const refDomains = (bl.top_referring_domains || []).length
    ? bl.top_referring_domains.map((r) => `<tr><td>${esc(r.domain)}</td><td class="num">${val(r.authority)}</td><td class="num">${val(r.links, num)}</td></tr>`).join('')
    : blankRows(3);
  const anchors = (bl.top_anchors || []).length
    ? bl.top_anchors.map((a) => `<tr><td>${esc(a.anchor)}</td><td class="num">${val(a.share, (x) => `${x}%`)}</td></tr>`).join('')
    : blankRows(2);

  const asOf = (iso) => (iso ? `As of ${fmtDate(iso)}` : 'Date to be confirmed');

  return `<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>${esc(c.name)} SEO Baseline</title>
<style>
  @page { size: A4; margin: 16mm 0 18mm; }
  @page cover { margin: 0; }
  :root { --ink:#0f1b2d; --navy:#13294b; --muted:#5b6b82; --line:#e3e8ef; --soft:#f5f7fa; --accent:#e0a526;
          --good:#1f9d6b; --warn:#d98a0b; --poor:#d14343; --low:#6b7a90; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:Inter, 'DejaVu Sans', sans-serif; color:var(--ink); font-size:10pt; line-height:1.45; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .page { width:210mm; padding:2mm 16mm 0; page-break-after:always; }
  .page:last-child { page-break-after:auto; }

  /* Cover */
  .cover { page:cover; height:297mm; background:var(--navy); color:#fff; padding:28mm 20mm; display:flex; flex-direction:column; overflow:hidden; }
  .cover .brand { font-weight:700; letter-spacing:.14em; font-size:9pt; text-transform:uppercase; color:var(--accent); }
  .cover h1 { font-family:'Inter Display', Inter, sans-serif; font-size:40pt; line-height:1.05; margin:60mm 0 6mm; font-weight:700; }
  .cover .client { font-size:20pt; font-weight:600; }
  .cover .url { color:#b7c4d8; font-size:11pt; margin-top:2mm; }
  .cover .bar { width:28mm; height:3px; background:var(--accent); margin:10mm 0; }
  .cover .meta { display:grid; grid-template-columns:auto 1fr; gap:2mm 8mm; font-size:10pt; color:#d5deea; }
  .cover .meta span { color:#8ea2bf; }
  .cover .covers { margin-top:auto; display:grid; grid-template-columns:repeat(3,1fr); gap:6mm; }
  .cover .covers div { border-top:1px solid #36507a; padding-top:4mm; font-size:9pt; color:#c4d0e1; }
  .cover .covers strong { display:block; color:#fff; font-size:11pt; margin-bottom:1mm; }

  /* Headings */
  .eyebrow { font-size:8pt; letter-spacing:.14em; text-transform:uppercase; color:var(--accent); font-weight:700; }
  h2 { font-family:'Inter Display', Inter, sans-serif; font-size:22pt; margin:1mm 0 2mm; color:var(--navy); }
  .lead { color:var(--muted); margin:0 0 7mm; max-width:150mm; }
  h3 { font-size:11.5pt; color:var(--navy); margin:7mm 0 3mm; }
  .src { font-size:8pt; color:var(--muted); }
  .muted { color:var(--muted); font-size:8pt; font-weight:400; }
  .empty { color:#a6b2c3; }

  /* Snapshot tiles */
  .tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:4mm; }
  .tiles.three { grid-template-columns:repeat(3,1fr); }
  .tile { background:var(--soft); border-radius:3mm; padding:5mm; }
  .tile-num { font-family:'Inter Display', Inter, sans-serif; font-size:20pt; font-weight:700; color:var(--navy); line-height:1.1; }
  .tile-label { font-size:8.5pt; color:var(--ink); margin-top:1.5mm; font-weight:600; }
  .tile-sub { font-size:7.5pt; color:var(--muted); }

  /* Score rings */
  .scores { border:1px solid var(--line); border-radius:3mm; padding:3mm 5mm; }
  .score-row { display:flex; align-items:center; gap:6mm; padding:3mm 0; }
  .score-row + .score-row { border-top:1px solid var(--line); }
  .device { width:22mm; font-weight:700; color:var(--navy); }
  .ring { width:30mm; text-align:center; }
  .ring-track { fill:none; stroke:#edf1f6; stroke-width:7; }
  .ring-val { fill:none; stroke-width:7; stroke-linecap:round; }
  .ring-val.good { stroke:var(--good); } .ring-val.warn { stroke:var(--warn); } .ring-val.poor { stroke:var(--poor); }
  .ring-num { font-size:20px; font-weight:700; fill:var(--ink); }
  .ring-num.good { fill:var(--good); } .ring-num.warn { fill:var(--warn); } .ring-num.poor { fill:var(--poor); }
  .ring-label { font-size:8pt; color:var(--muted); margin-top:-1mm; }
  .legend { display:flex; gap:5mm; font-size:7.5pt; color:var(--muted); margin-top:2mm; }
  .legend i { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:4px; vertical-align:middle; }

  /* Tables */
  table.data { width:100%; border-collapse:collapse; font-size:9pt; }
  table.data th { text-align:left; font-size:7.5pt; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); font-weight:600; border-bottom:1.5px solid var(--navy); padding:2mm 2mm; }
  table.data td { border-bottom:1px solid var(--line); padding:2.2mm 2mm; vertical-align:top; }
  table.data .num { text-align:right; white-space:nowrap; }
  table.data td.area { color:var(--muted); white-space:nowrap; width:24mm; }
  table.data td.url { color:var(--muted); font-size:8pt; }
  .pill { display:inline-block; padding:.6mm 2.4mm; border-radius:10mm; font-size:7.5pt; font-weight:600; white-space:nowrap; }
  .pill.good { background:#e3f5ed; color:var(--good); } .pill.warn { background:#fdf1dc; color:#a86a05; }
  .pill.poor { background:#fbe5e5; color:var(--poor); } .pill.low { background:#eef1f5; color:var(--low); }
  .pos { display:inline-block; min-width:8mm; text-align:center; padding:.5mm 1.5mm; border-radius:1.5mm; font-weight:700; }
  .pos.top3 { background:#e3f5ed; color:var(--good); } .pos.top10 { background:#e8f0fb; color:#2c5ea8; }
  .pos.top20 { background:#fdf1dc; color:#a86a05; } .pos.low, .pos.none { background:#eef1f5; color:var(--low); }

  .two { display:grid; grid-template-columns:1fr 1fr; gap:8mm; }
  .kv { display:flex; justify-content:space-between; gap:4mm; border-bottom:1px solid var(--line); padding:1.8mm 0; font-size:9pt; }
  .kv span { color:var(--muted); }

  .awaiting { background:repeating-linear-gradient(-45deg,#fbfcfd,#fbfcfd 6px,#f3f6f9 6px,#f3f6f9 12px); border:1px dashed #c9d3e0; border-radius:2mm; padding:3mm 4mm; color:var(--muted); font-size:8.5pt; margin-bottom:3mm; }

  /* Distribution */
  .dist { border:1px solid var(--line); border-radius:3mm; padding:4mm 5mm; }
  .dist-row { display:grid; grid-template-columns:24mm 1fr 12mm; align-items:center; gap:3mm; padding:1.2mm 0; }
  .dist-label { font-size:8.5pt; color:var(--muted); }
  .dist-track { height:4mm; background:#f0f3f7; border-radius:1mm; }
  .dist-bar { height:100%; border-radius:1mm; }
  .b0 { background:var(--good); } .b1 { background:#2c5ea8; } .b2 { background:var(--warn); } .b3, .b4 { background:#9aa8bb; } .b5 { background:#d5dce6; }
  .dist-num { text-align:right; font-weight:700; }

  h3, .awaiting { break-after:avoid; }
  tr, .tile, .score-row, .dist { break-inside:avoid; }
</style></head><body>

<section class="page cover">
  <div class="brand">${esc(c.prepared_by)}</div>
  <h1>SEO Baseline<br>Report</h1>
  <div class="client">${esc(c.name)}</div>
  <div class="url">${esc(c.url.replace(/^https?:\/\//, ''))}</div>
  <div class="bar"></div>
  <div class="meta">
    <span>Report date</span><div>${esc(fmtDate(c.report_date))}</div>
    <span>Purpose</span><div>Starting point for measuring SEO progress</div>
  </div>
  <div class="covers">
    <div><strong>Site health</strong>Speed, Core Web Vitals, accessibility and technical issues.</div>
    <div><strong>Keyword rankings</strong>Where the site ranks today for location and service searches.</div>
    <div><strong>Backlink profile</strong>Who links to the site and how strong those links are.</div>
  </div>
</section>

<section class="page">
  <div class="eyebrow">01 · At a glance</div>
  <h2>Baseline snapshot</h2>
  <p class="lead">These figures are the starting point. Each monthly report compares against them to show what has moved since onboarding.</p>
  <div class="tiles">
    ${snapshot.map((s) => `<div class="tile"><div class="tile-num">${val(s.value)}</div><div class="tile-label">${esc(s.label)}</div><div class="tile-sub">${esc(s.sub)}</div></div>`).join('')}
  </div>

  <h3>Lighthouse scores</h3>
  <div class="scores">
    ${scoreRow('Mobile', sh.mobile)}
    ${scoreRow('Desktop', sh.desktop)}
  </div>
  <div class="legend"><span><i style="background:var(--good)"></i>90–100 good</span><span><i style="background:var(--warn)"></i>50–89 needs work</span><span><i style="background:var(--poor)"></i>0–49 poor</span><span>Source: ${esc(sh.source)}, ${esc(fmtDate(sh.audited_on))}</span></div>

  <h3>Platform</h3>
  <div class="two"><div>${platform.slice(0, Math.ceil(platform.length / 2)).join('')}</div><div>${platform.slice(Math.ceil(platform.length / 2)).join('')}</div></div>
</section>

<section class="page">
  <div class="eyebrow">02 · Site health</div>
  <h2>Speed and technical health</h2>
  <p class="lead">Core Web Vitals are Google's page-experience signals. Mobile matters most because Google ranks the mobile version of the site.</p>
  <table class="data">
    <thead><tr><th>Metric</th><th class="num">Mobile</th><th></th><th class="num">Desktop</th><th></th></tr></thead>
    <tbody>${vitalsRows}
      <tr><td><strong>Page weight</strong><div class="muted">Total download size · aim under 2 MB</div></td>
        <td class="num">${val(sh.mobile?.page_weight_kb, (x) => `${(x / 1024).toFixed(1)} MB`)}</td><td>${has(sh.mobile?.page_weight_kb) ? pill(sh.mobile.page_weight_kb <= 2048 ? 'good' : sh.mobile.page_weight_kb <= 3072 ? 'warn' : 'poor') : ''}</td>
        <td class="num">${val(sh.desktop?.page_weight_kb, (x) => `${(x / 1024).toFixed(1)} MB`)}</td><td>${has(sh.desktop?.page_weight_kb) ? pill(sh.desktop.page_weight_kb <= 2048 ? 'good' : sh.desktop.page_weight_kb <= 3072 ? 'warn' : 'poor') : ''}</td></tr>
    </tbody>
  </table>
  <div class="src" style="margin-top:2mm">Lab measurements from a single Lighthouse run; scores vary by about ±5–15 points between runs.</div>

  <h3>Issues found</h3>
  ${(sh.issues || []).length ? '' : awaiting(sh.source)}
  <table class="data">
    <thead><tr><th style="width:20mm">Priority</th><th>Area</th><th>Issue</th></tr></thead>
    <tbody>${issues || blankRows(3)}</tbody>
  </table>
</section>

<section class="page">
  <div class="eyebrow">03 · Keyword rankings</div>
  <h2>Location and service rankings</h2>
  <p class="lead">Google UK positions for the keywords this campaign targets. Position 1–3 wins most clicks; page one is positions 1–10. <span class="src">${esc(rk.source)} · ${asOf(rk.as_of)}</span></p>
  <div class="two" style="grid-template-columns:1.25fr 1fr; align-items:start">
    <div>${distribution(allKw)}</div>
    <div class="tiles three" style="grid-template-columns:1fr 1fr">
      <div class="tile"><div class="tile-num">${allKw.length ? allKw.length : dash}</div><div class="tile-label">Keywords tracked</div></div>
      <div class="tile"><div class="tile-num">${allKw.length ? ranked.length : dash}</div><div class="tile-label">Ranking in top 100</div></div>
      <div class="tile"><div class="tile-num">${allKw.length ? top10 : dash}</div><div class="tile-label">On page one</div></div>
      <div class="tile"><div class="tile-num">${allKw.length ? allKw.filter((k) => has(k.position) && k.position <= 3).length : dash}</div><div class="tile-label">In top 3</div></div>
    </div>
  </div>
  ${kwTable('Location keywords', rk.location || [], rk.source)}
  ${kwTable('Service keywords', rk.service || [], rk.source)}
</section>

<section class="page">
  <div class="eyebrow">04 · Backlink profile</div>
  <h2>Who links to the site</h2>
  <p class="lead">Links from other relevant, trusted websites are one of Google's strongest ranking signals. Quality matters more than volume. <span class="src">${esc(bl.source)} · ${asOf(bl.as_of)}</span></p>
  ${blHas ? '' : awaiting(bl.source)}
  <div class="tiles three">${metrics}</div>
  <div class="two">
    <div>
      <h3>Top referring domains</h3>
      <table class="data"><thead><tr><th>Domain</th><th class="num">Authority</th><th class="num">Links</th></tr></thead><tbody>${refDomains}</tbody></table>
    </div>
    <div>
      <h3>Top anchor text</h3>
      <table class="data"><thead><tr><th>Anchor</th><th class="num">Share</th></tr></thead><tbody>${anchors}</tbody></table>
    </div>
  </div>
</section>

</body></html>`;
}

(async () => {
  const html = render();
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath.replace(/\.pdf$/, '.html'), html);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  // The cover prints on its own with no footer, then is merged in front of the body pages.
  const footer = `<div style="width:100%;margin:0 16mm;padding-top:2mm;border-top:1px solid #e3e8ef;display:flex;justify-content:space-between;font-family:Inter,sans-serif;font-size:7px;color:#5b6b82">
    <span>${esc(d.client.name)} · SEO Baseline Report · ${esc(d.client.prepared_by)}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`;
  const coverPdf = outPath.replace(/\.pdf$/, '.cover.tmp.pdf');
  const bodyPdf = outPath.replace(/\.pdf$/, '.body.tmp.pdf');
  await page.pdf({ path: coverPdf, printBackground: true, preferCSSPageSize: true, pageRanges: '1' });
  await page.pdf({ path: bodyPdf, printBackground: true, preferCSSPageSize: true, pageRanges: '2-', displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: footer });
  execFileSync('pdfunite', [coverPdf, bodyPdf, outPath]);
  fs.unlinkSync(coverPdf);
  fs.unlinkSync(bodyPdf);
  await browser.close();
  console.log(`Wrote ${outPath}`);
})();
