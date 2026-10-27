// Design Agent: palette, typography, layout and art direction.
const { llm } = require('./llm');

const DESIGN_SCHEMA = `{"palette":{"bg":"#hex dark or rich","fg":"#hex readable on bg","accent":"#hex","accent2":"#hex"},"headingFont":"serif|sans|display","layout":"bold|minimal|split","mood":"3 words","imagery":"one sentence art direction for the hero visual","motif":"single emoji or symbol used as brand mark"}`;

const design = (type, idea, brand, tone, r, copy) => llm(
  'You are the Design Agent on a creative team. Choose a distinctive, accessible visual direction (WCAG AA contrast between fg and bg). Return ONLY valid JSON, no prose.',
  `Idea/title: ${idea}\nBrand/company: ${brand || 'n/a'}\nTone: ${tone}\nFormat: ${type}\nAngle: ${r.angle}\nCopy headline: ${JSON.stringify(copy).slice(0, 400)}\n\nJSON schema:\n${DESIGN_SCHEMA}`);

module.exports = { design };
