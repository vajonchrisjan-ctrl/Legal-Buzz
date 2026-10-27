// Writing Agent: ads, proposal and post copy.
const { llm } = require('./llm');

const SCHEMAS = {
  ads: `{"meta":{"headline":"max 40 chars","primary":"max 125 chars","cta":"2-3 words"},"google":{"headlines":["max 30 chars x3"],"descriptions":["max 90 chars x2"]},"linkedin":{"intro":"max 150 chars","headline":"max 70 chars","cta":"2-3 words"}}`,
  proposal: `{"title":"","subtitle":"","summary":"2-3 sentences","problem":"2-3 sentences","solution":"2-3 sentences","scope":["4-6 deliverables"],"timeline":[{"phase":"","duration":"","detail":""}],"investment":[{"item":"","price":""}],"next_steps":"1-2 sentences"}`,
  post: `{"hook":"first line, max 90 chars","body":"80-140 words, short paragraphs separated by \\n\\n","hashtags":["3-5"],"cta":"one line","carousel":[{"title":"max 6 words","text":"max 20 words"}]}  (carousel: 5 slides)`,
};

const write = (type, idea, brand, tone, r) => llm(
  'You are the Writing Agent on a creative team. Write sharp, specific, human copy. No clichés. Return ONLY valid JSON, no prose.',
  `Idea/title: ${idea}\nBrand/company: ${brand || 'n/a'}\nTone: ${tone}\nResearch brief: ${JSON.stringify(r)}\n\nWrite ${type} creative. JSON schema:\n${SCHEMAS[type]}`);

module.exports = { write };
