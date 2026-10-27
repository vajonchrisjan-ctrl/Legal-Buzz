// Offline stand-ins for the three agents (used when no API key is set).
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

module.exports = { demo };
