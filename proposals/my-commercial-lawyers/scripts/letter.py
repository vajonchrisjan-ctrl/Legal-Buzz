# Cover letter for the My Commercial Lawyers proposal, in the legalbuzz proposal design.
import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from comp import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'tpl/exp.pretty.html'), encoding='utf-8').read().split('\n')
L = lambda a, b: '\n'.join(TPL[a - 1:b])
FIRM = 'My Commercial Lawyers'
DATE = '13 October 2026'

head = L(1, 311)
head = re.sub(r'<title>.*?</title>', f'<title>A letter to {FIRM} | legalbuzz</title>', head)
head = re.sub(r'content="How Anchored Family Law[^"]*"', f'content="Why {FIRM} is first on the map and missing from the AI answer, and what we would do about it."', head)
head = head.replace('Growth proposal for Anchored Family Law | legalbuzz', f'A letter to {FIRM} | legalbuzz')
head = head.replace('href="/assets/styles-CK15uquF.css"', 'href="assets/styles-CK15uquF.css"')
head = re.sub(r'(href|src)="/(?!/)', r'\1="https://legalbuzz.co/', head)
head = head.replace('<link rel="preload" as="image" href="https://legalbuzz.co/assets/anchored-logo-white-C58Horq_.svg" />', '')
head = head.replace('class="fixed inset-x-0 top-0 z-50 border-b', 'class="relative inset-x-0 top-0 z-50 border-b')
head = head.replace('</head>', '''<style>@page { size: 1280px 1810px; margin: 0; } html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } .mcl-logo { filter: brightness(0) invert(1); }
.letter p.lp { font-size: 16.5px; } .letter p.lede { font-size: 19px; }</style>
  </head>''')

def lp(t, cls=''):
    return f'<p class="lp my-4 max-w-3xl leading-relaxed text-foreground/85 {cls}">{t}</p>'

hero = f'''<main class="bg-background">
<section class="bg-primary pt-10 pb-10 text-primary-foreground"><div class="band-x mx-auto max-w-6xl">
<div class="flex flex-wrap items-center justify-between gap-6"><div>
<img src="mcl-logo.png" alt="{FIRM}" class="mcl-logo mb-5 h-14 w-auto" />
<p class="text-xs font-bold tracking-[0.2em] text-accent uppercase">A LETTER FOR {FIRM.upper()} · {DATE.upper()}</p></div></div>
<h1 class="mt-6 font-display text-5xl font-bold leading-[0.95] lg:text-7xl">You have already won the map. Now win the answer.</h1>
</div></section>'''

body = f'''<section class="pt-10 pb-6"><div class="band-x mx-auto max-w-6xl letter">
<p class="text-sm text-muted-foreground">{DATE}</p>
{lp(b('Dear My Commercial Lawyers team,'), 'lede')}
{lp('You probably do not think you need an agency. On paper, you are right. When a contractor in London searches "construction dispute solicitor london", your Google profile is the first firm on the map, ahead of Fenwick Elliott. You publish every month: twenty-two guides this year alone. You have an SEO specialist on the team. Your technical SEO score is 100 out of 100. Most firms we write to would swap places with you tomorrow.')}
{lp('So why are we writing? Because the search that wins the instruction has moved, and it has moved past you. Above the map you top, Google now shows an AI answer. For that exact search it names six firms: Russell-Cooke, Osbornes Law, Forsters, B P Collins, JHA and Trowers &amp; Hamlins. It does not name you. A contractor reads that answer before they ever see the map.')}
{stats([('27 / 0', 'AI answers that use your pages as a source / AI answers that say your name'), ('190 of 195', 'monthly Google visits that land on your homepage; your service pages earn none'), ('6', 'firms the AI answer recommends for "construction dispute solicitor london". You are #1 on the map for the same search')], cols=3)}
{plain('Google trusts you enough to put you on the map. AI does not know enough about you to say your name. It cannot see who your barristers are, it cannot find your regulator, and every guide on your site is signed by an author who is not on your team page. So it borrows your expertise and recommends somebody else.')}
{h3('What we would do')}
{lp('The full plan is in the proposal with this letter. In short, three stages, in the order your client makes the decision.')}
{stages([
    ('Be seen', 'Can Google and AI find you?', 'One London construction disputes hub replaces the seven pages now competing for the same search. Each service page is rebuilt to own one question. Seventeen of your twenty-four service and location pages rank for nothing today.', 'Website not in the top 100 for your best search'),
    ('Be trusted', 'Does AI recommend you?', 'A profile for every barrister and solicitor, your Bar Standards Board reference in the code AI reads, every guide signed by a lawyer, and listings in Legal 500 and Chambers, the sources AI already cites in your topics.', 'Cited 27 times, named 0 times'),
    ('Be chosen', 'Do they call you, not the firm next door?', 'Tap-to-call in the header, your "scope and fee before work begins" promise on every page, and the reviews behind your map listing shown on your own site.', 'Services start on screen six of a phone'),
])}
{h3('Why legalbuzz')}
{lp('We only work with law firms, and we are measured on instructions, not traffic. Before legalbuzz we ran Conveyancer Plus, a sales team that only got paid when an enquiry became an instruction.')}
{cards([
    ('J Scott &amp; Co, Maidenhead.', 'Enquiries from 15 to 77 a month in six months. ChatGPT now names them first for a conveyancer in Maidenhead.'),
    ('Deen &amp; Co, Canary Wharf.', 'A London specialist up against national firms. 33 enquiries in one month, 29% of them from ChatGPT, and 7,017 AI citations.'),
    ('Signature Law, Romford.', 'Enquiries up 300% in six months, with service and location pages built the way we would build yours.'),
])}
{h3('Why now')}
{lp('While AI recommends someone else, your next client hears another firm’s name before they see yours on the map, and those six firms collect the reviews and citations that make them harder to move each month. You have done the hardest part. What is left is the part that compounds.')}
{h3('The offer')}
{lp('With buzzExpansion we build you a new AI-ready site at no cost, and your first month is £1. If you would rather keep your current site, your first month is half price. Six-month term, then month to month. The audit is yours to keep either way, and everything we write follows the BSB Handbook: no promised outcomes.')}
{lp(b('The next step is thirty minutes.') + ' We walk you through the audit, page by page, and you decide. Reply to this email, call us on 020 4652 0997, or book a time at legalbuzz.co/book-a-call.')}
{lp('Yours sincerely,')}
<div class="mt-6 grid max-w-3xl gap-6 sm:grid-cols-2">
<div class="flex items-center gap-4"><img src="assets/george-profile-IpPg1vSs.jpeg" alt="George Levett" class="h-16 w-16 rounded-full object-cover grayscale" /><div><p class="font-display text-lg font-bold">George Levett</p><p class="text-xs font-semibold tracking-[0.14em] text-primary uppercase">Co-founder, Search &amp; AI Visibility</p></div></div>
<div class="flex items-center gap-4"><img src="assets/pj-singh.jpg" alt="PJ Singh" class="h-16 w-16 rounded-full object-cover grayscale" /><div><p class="font-display text-lg font-bold">PJ Singh</p><p class="text-xs font-semibold tracking-[0.14em] text-primary uppercase">Co-founder, Sales &amp; Client Growth</p></div></div>
</div>
<div class="my-10 max-w-3xl rounded-xl border-l-4 border-accent bg-accent/15 px-6 py-5">{lp(b('P.S.') + ' Search "construction dispute solicitor london" on Google today. Find yourself on the map, then read the AI answer above it. That gap is the whole proposal.', '!my-0')}</div>
<p class="mt-8 border-t border-border pt-6 text-sm text-muted-foreground">legalbuzz · start@legalbuzz.co · 020 4652 0997 · 133 Ley Street, Ilford, Greater London, IG1 4BH · Figures: live audit of mycommerciallawyers.com and SE Ranking (Google UK and AI Search), {DATE}.</p>
</div></section></main>'''

page = head + '\n' + hero + body + '\n  </body>\n</html>'
open(os.path.join(ROOT, 'build/letter.html'), 'w', encoding='utf-8').write(page)
print('written', len(page))
