// Design creative app — Research → Writing → Design agent pipeline.
// Zero dependencies. Uses the Anthropic API when ANTHROPIC_API_KEY is set, otherwise demo mode.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { API_KEY, MODEL } = require('./agents/llm');
const { research } = require('./agents/research');
const { write } = require('./agents/writing');
const { design } = require('./agents/design');
const { demo } = require('./agents/demo');

const PORT = process.env.PORT || 3000;
const PUBLIC = path.join(__dirname, 'public');
const sleep = ms => new Promise(r => setTimeout(r, ms));

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
