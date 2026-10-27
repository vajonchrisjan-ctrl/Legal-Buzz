// Shared Claude API caller used by all three agents.
const API_KEY = process.env.ANTHROPIC_API_KEY;
const MODEL = process.env.CLAUDE_MODEL || 'claude-sonnet-5-5';

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
module.exports = { llm, API_KEY, MODEL };
