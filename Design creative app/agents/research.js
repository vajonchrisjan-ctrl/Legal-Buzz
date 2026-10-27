// Research Agent: audience, pains, insights and the creative angle.
const { llm } = require('./llm');

const research = (idea, brand, tone) => llm(
  'You are the Research Agent on a creative team. Return ONLY valid JSON, no prose.',
  `Idea/title: ${idea}\nBrand/company: ${brand || 'n/a'}\nTone: ${tone}\n\nProduce audience research for creative work. JSON schema:\n{"audience":"who exactly","pains":["3 pain points"],"insights":["3 sharp insights"],"angle":"the single strongest creative angle","proof_points":["3 credible proof points / stats framed as claims to verify"],"keywords":["5 keywords"]}`);

module.exports = { research };
