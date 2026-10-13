// Pushes blocks that would cross a page edge onto the next page, leaving fixed top/bottom gutters.
(H, G) => {
  const abs = el => { const r = el.getBoundingClientRect(); return { t: r.top + scrollY, b: r.bottom + scrollY, h: r.height }; };
  const usable = H - 2 * G;
  const ATOMIC = 'p,h1,h2,h3,h4,li,figure,img,blockquote,iframe,svg,button,thead,.rounded-xl,.rounded-2xl,.rounded-lg,footer > div';
  const isHead = e => e && /^H[2-4]$/.test(e.tagName);
  // keep a heading (and a one-paragraph intro after it) on the same page as the block it introduces
  const leader = el => { let s = el; for (let i = 0; i < 2; i++) { const pv = s.previousElementSibling; if (!pv) break; if (isHead(pv)) { s = pv; break; } if (pv.tagName === 'P' && isHead(pv.previousElementSibling) && abs(pv).h < 160) { s = pv; continue; } break; } return s; };
  const setTop = (el, want) => { for (let i = 0; i < 3; i++) { const d = want - abs(el).t; if (Math.abs(d) < 0.5) break; el.style.marginTop = (parseFloat(getComputedStyle(el).marginTop) || 0) + d + 'px'; } };
  const push = (el, delta) => {
    if (el.tagName === 'TR') {
      const tr = document.createElement('tr'); const td = document.createElement('td');
      td.colSpan = el.children.length || 1; td.style.cssText = `height:${delta}px;padding:0;border:0;background:transparent`;
      tr.appendChild(td); tr.className = 'pg-spacer'; el.parentNode.insertBefore(tr, el); return;
    }
    const cs = getComputedStyle(el);
    const parent = el.parentElement, pcs = parent && getComputedStyle(parent);
    if (pcs && (pcs.display.includes('grid') || pcs.display.includes('flex')) ) {
      // move the whole row: push the container instead when it fits on a page
      if (abs(parent).h <= usable) return push(parent, delta);
    }
    const lead = isHead(el) ? el : leader(el);
    if (lead !== el) { const target = abs(el).t + delta; const lt = abs(lead).t; const k2 = Math.floor(target / H); if (lt < k2 * H) { setTop(lead, k2 * H + G); return; } }
    setTop(el, abs(el).t + delta);
  };
  const place = el => {
    const r = abs(el); if (r.h === 0) return;
    const k = Math.floor(r.t / H), top = k * H + G, bottom = (k + 1) * H - G;
    if (r.t < top && r.h <= usable && el.matches(ATOMIC + ',tr')) { push(el, top - r.t); return; }
    if (isHead(el) && el.nextElementSibling && r.b <= bottom && r.b > bottom - 220 && abs(el.nextElementSibling).b > bottom) { push(el, (k + 1) * H + G - r.t); return; }
    if (r.b <= bottom) return;
    const atomic = el.matches(ATOMIC + ',tr') && r.h <= usable;
    const kids = [...el.children].filter(c => abs(c).h > 0 && getComputedStyle(c).position !== 'absolute');
    if (atomic || kids.length === 0) {
      if (r.h <= usable) push(el, (k + 1) * H + G - r.t);
      return;
    }
    for (const c of kids) place(c);
  };
  // every numbered section, the closing band and the footer band start on a fresh page
  const starts = [...document.querySelectorAll('section[id^="s"], main section.bg-primary.py-20, body > section.bg-primary')];
  const blocks = [...document.querySelectorAll('header, main > section, main > nav, main > div > section, main > div > div, body > section, body > footer')];
  for (const el of blocks) {
    if (starts.includes(el)) {
      let t = abs(el).t;
      // if only the previous section's bottom padding spilled onto this page, trim it instead of leaving a blank page
      const spill = t - Math.floor(t / H) * H;
      if (t > 0 && spill > 2 && spill < 200) {
        const secs = [...document.querySelectorAll('section')].filter(x => abs(x).b <= t + 1 && x !== el && !x.contains(el));
        const prev = secs[secs.length - 1];
        if (prev) { const pb = parseFloat(getComputedStyle(prev).paddingBottom) || 0; if (pb >= spill) { prev.style.paddingBottom = (pb - spill) + 'px'; t = abs(el).t; } }
      }
      const k = Math.floor((t - 1) / H) + 1, target = k * H;
      if (t > 0 && Math.abs(t - (k - 1) * H) > 2) el.style.marginTop = (target - t) + 'px';
    }
    const kids = [...el.children];
    for (const c of kids) place(c);
  }
  // audit: text that ended up inside a gutter
  const bad = [];
  for (const e of document.querySelectorAll('p,h1,h2,h3,h4,td,th,li,span,a')) {
    if (e.children.length > 3) continue; const r = abs(e); if (r.h === 0 || r.h > usable) continue;
    const off = ((r.t % H) + H) % H, offb = ((r.b % H) + H) % H;
    if ((off < G - 6 && r.t > 10) || (Math.floor(r.t / H) !== Math.floor((r.b - 1) / H))) bad.push(Math.floor(r.t / H) + 1 + ':' + e.tagName + ':' + (e.innerText || '').slice(0, 40));
  }
  window.__bad = bad;
  return document.body.scrollHeight;
}
