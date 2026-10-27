// Creative Studio — Research → Writing → Design agent pipeline.
// Zero dependencies. Uses the Anthropic API when ANTHROPIC_API_KEY is set, otherwise demo mode.
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const API_KEY = process.env.ANTHROPIC_API_KEY;
const MODEL = process.env.CLAUDE_MODEL || 'claude-sonnet-5-5';
const PUBLIC = path.join(__dirname, 'public');

// ---------- LLM helper ----------
async function llm(system, user) {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': API_KEY, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify({ model: MODEL, max_tokens: 4000, system, messages: [{ role: 'user', content: user }] }),
  });
  if (!res.ok) throw new Error(`Anthropic API ${res.status}: ${(await res.text()).slice(0, 300)}`);
  const j = await res.json();
  const text = j.content.map(b => b.text || '').join('');
  const a = text.indexOf('{'), b = text.lastIndexOf('}');
  if (a < 0 || b < 0) throw new Error('Agent returned no JSON');
  return JSON.parse(text.slice(a, b + 1));
}
const sleep = ms => new Promise(r => setTimeout(r, ms));

// ---------- Agent prompts ----------
const SCHEMAS = {
  ads: `{"meta":{"headline":"max 40 chars","primary":"max 125 chars","cta":"2-3 words"},"google":{"headlines":["max 30 chars x3"],"descriptions":["max 90 chars x2"]},"linkedin":{"intro":"max 150 chars","headline":"max 70 chars","cta":"2-3 words"}}`,
  proposal: `{"title":"","subtitle":"","summary":"2-3 sentences","problem":"2-3 sentences","solution":"2-3 sentences","scope":["4-6 deliverables"],"timeline":[{"phase":"","duration":"","detail":""}],"investment":[{"item":"","price":""}],"next_steps":"1-2 sentences"}`,
  post: `{"hook":"first line, max 90 chars","body":"80-140 words, short paragraphs separated by \\n\\n","hashtags":["3-5"],"cta":"one line","carousel":[{"title":"max 6 words","text":"max 20 words"}]}  (carousel: 5 slides)`,
};
const DESIGN_SCHEMA = `{"palette":{"bg":"#hex dark or rich","fg":"#hex readable on bg","accent":"#hex","accent2":"#hex"},"headingFont":"serif|sans|display","layout":"bold|minimal|split","mood":"3 words","imagery":"one sentence art direction for the hero visual","motif":"single emoji or symbol used as brand mark"}`;

const research = (idea, brand, tone) => llm(
  'You are the Research Agent on a creative team. Return ONLY valid JSON, no prose.',
  `Idea/title: ${idea}\nBrand/company: ${brand || 'n/a'}\nTone: ${tone}\n\nProduce audience research for creative work. JSON schema:\n{"audience":"who exactly","pains":["3 pain points"],"insights":["3 sharp insights"],"angle":"the single strongest creative angle","proof_points":["3 credible proof points / stats framed as claims to verify"],"keywords":["5 keywords"]}`);

const write = (type, idea, brand, tone, r) => llm(
  'You are the Writing Agent on a creative team. Write sharp, specific, human copy. No clichés. Return ONLY valid JSON, no prose.',
  `Idea/title: ${idea}\nBrand/company: ${brand || 'n/a'}\nTone: ${tone}\nResearch brief: ${JSON.stringify(r)}\n\nWrite ${type} creative. JSON schema:\n${SCHEMAS[type]}`);

const design = (type, idea, brand, tone, r, copy) => llm(
  'You are the Design Agent on a creative team. Choose a distinctive, accessible visual direction (WCAG AA contrast between fg and bg). Return ONLY valid JSON, no prose.',
  `Idea/title: ${idea}\nBrand/company: ${brand || 'n/a'}\nTone: ${tone}\nFormat: ${type}\nAngle: ${r.angle}\nCopy headline: ${JSON.stringify(copy).slice(0, 400)}\n\nJSON schema:\n${DESIGN_SCHEMA}`);

// ---------- Demo mode (no API key) ----------
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
const trim = (s, n) => s.length <= n ? s : s.slice(0, n - 1).trimEnd() + '…';
const PALETTES = [
  { bg: '#0f172a', fg: '#f8fafc', accent: '#f59e0b', accent2: '#38bdf8' },
  { bg: '#1e1b4b', fg: '#eef2ff', accent: '#f472b6', accent2: '#a78bfa' },
  { bg: '#052e2b', fg: '#ecfdf5', accent: '#34d399', accent2: '#fbbf24' },
  { bg: '#1c1917', fg: '#fafaf9', accent: '#fb7185', accent2: '#fdba74' },
];
const hash = s => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
const demo = {
  research: (idea, brand) => ({
    audience: `Decision-makers who are actively looking for help with ${idea}`,
    pains: ['Too many options, unclear which to trust', 'Past providers over-promised and under-delivered', 'No time to research properly'],
    insights: ['Buyers choose the option that feels lowest-risk, not cheapest', 'Specific outcomes beat generic claims', 'Speed of response is a trust signal'],
    angle: `Make ${idea} feel simple, safe and fast${brand ? ` with ${brand}` : ''}`,
    proof_points: ['Client outcome or testimonial (to verify)', 'Years of experience (to verify)', 'Turnaround time guarantee (to verify)'],
    keywords: idea.toLowerCase().split(/\s+/).filter(w => w.length > 3).slice(0, 3).concat(['trusted', 'fast']),
  }),
  write: (type, idea, brand) => {
    const B = brand || 'Us', T = cap(idea);
    if (type === 'ads') return {
      meta: { headline: trim(`${T}, made simple`, 40), primary: trim(`Stop guessing. ${B} gives you a clear, low-risk path to ${idea} — with real people on the other end.`, 125), cta: 'Get a quote' },
      google: { headlines: [trim(T, 30), trim(`Trusted ${idea}`, 30), 'Free Initial Advice'], descriptions: [trim(`Clear pricing, fast turnaround and a named expert on your case. Talk to ${B} today.`, 90), 'No jargon, no surprises. Book a free call and get a plan within 24 hours.'] },
      linkedin: { intro: trim(`Most teams overcomplicate ${idea}. Here's the shortcut.`, 150), headline: trim(`${T} without the headache`, 70), cta: 'Learn more' },
    };
    if (type === 'proposal') return {
      title: `${T} Proposal`, subtitle: `Prepared by ${B}`,
      summary: `This proposal sets out how ${B} will deliver ${idea} with a clear scope, fixed timeline and transparent pricing.`,
      problem: `Teams exploring ${idea} face unclear options, inconsistent advice and little visibility on cost or timing.`,
      solution: `We provide an end-to-end approach: discovery, a tailored plan, delivery and review — with a single point of contact throughout.`,
      scope: ['Discovery workshop & requirements', 'Tailored strategy and plan', 'Core delivery', 'Quality review and revisions', 'Handover and reporting'],
      timeline: [{ phase: 'Discover', duration: 'Week 1', detail: 'Goals, constraints, success measures' }, { phase: 'Plan', duration: 'Week 2', detail: 'Approach and sign-off' }, { phase: 'Deliver', duration: 'Weeks 3–6', detail: 'Build, review, iterate' }, { phase: 'Handover', duration: 'Week 7', detail: 'Reporting and next steps' }],
      investment: [{ item: 'Discovery & plan', price: '£—' }, { item: 'Delivery', price: '£—' }, { item: 'Review & handover', price: '£—' }],
      next_steps: 'Confirm scope, agree start date, and we will issue the engagement letter within 48 hours.',
    };
    return {
      hook: trim(`${T}: what nobody tells you first.`, 90),
      body: `Most people approach ${idea} backwards — they start with tools and end with regret.\n\nHere's what works instead:\n\n1. Define the outcome before the method.\n2. Pick one measure of success.\n3. Get a second opinion from someone who's done it before.\n\nIt takes an afternoon, and it saves months.`,
      hashtags: ['#' + idea.split(/\s+/)[0].replace(/\W/g, ''), '#Strategy', '#Growth'], cta: 'Want the checklist? Comment "YES" and I\'ll send it.',
      carousel: [{ title: 'Start here', text: 'A 5-slide primer you can use today.' }, { title: 'Outcome first', text: 'Define what "done" looks like before choosing a method.' }, { title: 'One metric', text: 'Pick a single number that proves it worked.' }, { title: 'Second opinion', text: 'Ask someone who has done it before you commit.' }, { title: 'Take the next step', text: `Talk to ${B} — we\'ll map it out with you.` }],
    };
  },
  design: (idea, type) => {
    const h = hash(idea + type), p = PALETTES[h % PALETTES.length];
    return { palette: p, headingFont: ['serif', 'sans', 'display'][h % 3], layout: ['bold', 'minimal', 'split'][(h >> 3) % 3], mood: 'confident, clear, modern', imagery: `Abstract geometric hero in ${p.accent} and ${p.accent2} on a dark field`, motif: ['◆', '●', '▲', '✦'][h % 4] };
  },
};

// ---------- Pipeline ----------
async function run(body, send) {
  const idea = String(body.idea || '').trim().slice(0, 500);
  const brand = String(body.brand || '').trim().slice(0, 100);
  const tone = String(body.tone || 'professional and warm').slice(0, 60);
  const types = ['ads', 'proposal', 'post'];
  const live = !!API_KEY;
  send({ type: 'mode', live, model: live ? MODEL : null });

  send({ type: 'agent', agent: 'research', status: 'working', note: 'Profiling audience, pains and angle…' });
  const r = live ? await research(idea, brand, tone) : (await sleep(900), demo.research(idea, brand));
  send({ type: 'agent', agent: 'research', status: 'done', note: r.angle, data: r });

  send({ type: 'agent', agent: 'writing', status: 'working', note: 'Drafting ads, proposal and post copy…' });
  const copy = live ? Object.fromEntries(await Promise.all(types.map(async t => [t, await write(t, idea, brand, tone, r)])))
    : (await sleep(1100), Object.fromEntries(types.map(t => [t, demo.write(t, idea, brand)])));
  send({ type: 'agent', agent: 'writing', status: 'done', note: 'Copy ready for all 3 formats' });

  send({ type: 'agent', agent: 'design', status: 'working', note: 'Choosing palette, type and layout…' });
  const des = live ? Object.fromEntries(await Promise.all(types.map(async t => [t, await design(t, idea, brand, tone, r, copy[t])])))
    : (await sleep(900), Object.fromEntries(types.map(t => [t, demo.design(idea, t)])));
  send({ type: 'agent', agent: 'design', status: 'done', note: 'Visual direction set' });

  send({ type: 'result', result: { idea, brand, research: r, outputs: Object.fromEntries(types.map(t => [t, { copy: copy[t], design: des[t] }])) } });
}

// ---------- HTTP ----------
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/api/generate') {
    let raw = '';
    req.on('data', c => { raw += c; if (raw.length > 1e5) req.destroy(); });
    req.on('end', async () => {
      res.writeHead(200, { 'content-type': 'text/event-stream', 'cache-control': 'no-cache', connection: 'keep-alive' });
      const send = o => res.write(`data: ${JSON.stringify(o)}\n\n`);
      try {
        const body = JSON.parse(raw || '{}');
        if (!String(body.idea || '').trim()) throw new Error('Please enter a title or idea.');
        await run(body, send);
      } catch (e) { send({ type: 'error', message: e.message }); }
      res.end();
    });
    return;
  }
  const file = path.join(PUBLIC, req.url === '/' ? 'index.html' : path.normalize(req.url.split('?')[0]).replace(/^(\.\.[/\\])+/, ''));
  if (!file.startsWith(PUBLIC)) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end('Not found'); }
    res.writeHead(200, { 'content-type': MIME[path.extname(file)] || 'application/octet-stream' });
    res.end(data);
  });
}).listen(PORT, () => console.log(`Creative Studio on http://localhost:${PORT}  (${API_KEY ? 'LIVE: ' + MODEL : 'DEMO mode — set ANTHROPIC_API_KEY for live agents'})`));
