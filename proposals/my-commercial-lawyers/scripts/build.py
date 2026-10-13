import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from comp import *
import seo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = open(os.path.join(ROOT, 'tpl/exp.pretty.html'), encoding='utf-8').read().split('\n')
L = lambda a, b: '\n'.join(TPL[a - 1:b])  # 1-indexed inclusive line slice of the template

FIRM = 'My Commercial Lawyers'
SHORT = 'MCL'
DATE = '13 October 2026'
PEND = pending('Awaiting SE Ranking export')
PENDB = pending('To confirm with you')

def sub(s, extra=()):
    reps = list(extra) + [
        ('Anchored Family Law', FIRM), ('Anchored', SHORT),
        ('Prices are in Australian dollars, per month.', 'Prices are in pounds sterling, per month, plus VAT.'),
    ]
    for a, b_ in reps: s = s.replace(a, b_)
    return s

# ---------------------------------------------------------------- head + header
head = L(1, 311)
head = head.replace('<title>Growth proposal for Anchored Family Law | legalbuzz</title>', f'<title>Growth proposal for {FIRM} | legalbuzz</title>')
head = re.sub(r'content="How Anchored Family Law[^"]*"', f'content="How {FIRM} gets found on Google, recommended by AI and chosen by UK businesses with commercial and construction disputes."', head)
head = head.replace('Growth proposal for Anchored Family Law | legalbuzz', f'Growth proposal for {FIRM} | legalbuzz')
head = head.replace('href="/assets/styles-CK15uquF.css"', 'href="assets/styles-CK15uquF.css"')
head = re.sub(r'(href|src)="/(?!/)', r'\1="https://legalbuzz.co/', head)
head = head.replace('<link rel="preload" as="image" href="https://legalbuzz.co/assets/anchored-logo-white-C58Horq_.svg" />', '')
# Static header for print (fixed headers repeat on every PDF page)
head = head.replace('class="fixed inset-x-0 top-0 z-50 border-b', 'class="relative inset-x-0 top-0 z-50 border-b')
PRINT_CSS = '''<style>
@page { size: 1280px 1810px; margin: 0; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.mcl-logo { filter: brightness(0) invert(1); }
</style>'''
head = head.replace('</head>', PRINT_CSS + '\n  </head>')

# ---------------------------------------------------------------- hero
CHIPS = ['Who we are', 'Your brief', 'Where MCL is today', 'Why Google and AI do not trust the site yet',
         'Who you are up against in London', 'What AI says about you', 'The action plan', 'The legalbuzz method',
         'Sales process analysis', 'Working together']
chip_hero = ''.join(f'<a href="#s{i}" class="inline-flex items-center gap-2 rounded-full border border-primary-foreground/25 px-4 py-2 text-sm font-semibold transition-colors hover:border-accent hover:bg-accent hover:text-accent-foreground"><span class="text-xs opacity-70">{i}</span>{t}</a>' for i, t in enumerate(CHIPS, 1))
chip_nav = ''.join(f'<a href="#s{i}" class="inline-flex shrink-0 items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-colors bg-surface text-foreground hover:bg-muted"><span class="text-xs text-muted-foreground">{i}</span>{t}</a>' for i, t in enumerate(CHIPS, 1))

hero = f'''<main class="bg-background">
<section class="bg-primary pt-16 pb-16 text-primary-foreground lg:pt-20 lg:pb-20"><div class="band-x mx-auto max-w-6xl">
<div class="flex flex-wrap items-center justify-between gap-6"><div>
<img src="mcl-logo.png" alt="{FIRM}" class="mcl-logo mb-5 h-14 w-auto sm:h-16" />
<p class="text-xs font-bold tracking-[0.2em] text-accent uppercase">PREPARED FOR {FIRM.upper()} · {DATE.upper()}</p></div>
<div class="rounded-md bg-background p-1" style="width: 160px"><iframe title="legalbuzz on GoodFirms" src="https://widget.goodfirms.co/?cid=224727&amp;wt=goodfirms-widget-t6&amp;wp=star-no-review" width="100%" height="100" scrolling="no" style="border: 0; display: block"></iframe></div></div>
<h1 class="mt-6 font-display text-5xl font-bold leading-[0.95] lg:text-7xl">Be seen. Be trusted. Be chosen.</h1>
<p class="mt-8 max-w-4xl font-display text-2xl font-semibold leading-snug text-balance lg:text-3xl">A growth plan for {FIRM}</p>
<p class="mt-6 max-w-3xl text-lg leading-relaxed text-primary-foreground/75">How we would get {FIRM} ranking on Google, recommended by AI, and chosen by UK businesses with a commercial or construction dispute, in London and Croydon first, then nationally and for overseas clients.</p>
{stats([("0", "AI answers that name My Commercial Lawyers. 27 cite one of your pages without saying your name"),
        ("0.01%", "your share of UK AI answers across Google AI, ChatGPT, Perplexity and Gemini"),
        ("45", "out of 100: Google's mobile performance score for your homepage")], cols=3, dark=True)}
<div class="mt-8 flex flex-wrap gap-2">{chip_hero}</div>
<p class="mt-10 border-t border-primary-foreground/15 pt-6 text-sm text-primary-foreground/60">Prepared for the {FIRM} team · Prepared by George Levett and PJ Singh, legalbuzz · Data: live crawl of all 75 URLs on mycommerciallawyers.com, Google Lighthouse 12 (mobile), an iPhone-sized render, {DATE}. SE Ranking: Google UK database and AI Search (UK), October 2026.</p>
</div></section>
<nav aria-label="Proposal sections" class="border-b border-border bg-background/95"><div class="band-x mx-auto flex max-w-6xl flex-wrap gap-2 py-3">{chip_nav}</div></nav>'''

# ---------------------------------------------------------------- s1 Who we are (template, generic)
s1 = L(440, 705)
s1 = s1.replace('We know what a separating parent types at 11pm', 'We know what a contractor chasing an unpaid valuation types at 11pm')
s1 = s1.replace('including family law firms facing exactly the shift you are.', 'including specialist dispute firms facing exactly the shift you are.')
s1 = s1.replace('That is the answer we want ChatGPT and Google to give about Anchored Family Law when someone in Ballarat asks for a family lawyer, or when someone anywhere in Australia asks for a\n                fixed-fee or subscription family lawyer.',
                'That is the answer we want ChatGPT and Google to give about My Commercial Lawyers when someone in London asks for a construction dispute solicitor, or when a business anywhere in the UK, or overseas, asks who can help with an adjudication, an unpaid invoice or a breach of contract.')
s1 = s1.replace('Fix the site, build the Ballarat pillar, rebuild the four service pages.', 'Fix the site, build the London construction disputes pillar, consolidate the overlapping service pages.')
s1 = s1.replace('Not in the top 100 for any Ballarat search', '190 of 195 Google visits land on the homepage; service pages earn none')
s1 = s1.replace("Teach AI you are in Ballarat. Emma's profile, schema, Australian citations, reviews.", 'Teach AI who your barristers and solicitors are, where you are, and that you are regulated. Profiles, schema, UK legal citations, reviews.')
s1 = s1.replace('<span class="font-bold text-destructive">Today: </span>1.3% of AI answers', '<span class="font-bold text-destructive">Today: </span>0.01% of AI answers, named in none')
s1 = s1.replace('A site built to convert: awards, accreditations and reviews up front, phone in the header, prices visible, a Ballarat profile with forty reviews.', 'A site built to convert: barrister-led credentials and reviews up front, tap-to-call in the header, the "scope and fee before work begins" promise on every page.')
s1 = s1.replace("The site doesn't sell you: awards hidden, 2 Google reviews in Ballarat", 'Testimonials with no review platform behind them; services start on screen six of a phone')
s1 = re.sub(r'When someone does land on your site, it doesn\'t convince them to call\..*?so visits turn into calls and consults\.',
            'When someone does land on your site, the strongest proof you have is buried. Client testimonials sit on the homepage with nothing behind them that Google or AI can check, the regulatory status that sets you apart (barristers authorised by the Bar Standards Board for Direct Public Access and to conduct litigation) is only in the footer, and on a phone the phone number in the top bar cannot be tapped. The new site puts that proof up front on every page, so visits turn into calls and instructions.', s1, flags=re.S)
s1 = re.sub(r'<strong class="font-semibold text-foreground">In plain English:</strong> Your website is invisible.*?gaps a specialist can walk through\.',
            '<strong class="font-semibold text-foreground">In plain English:</strong> Your site is not the problem most firms have. It is fresh, long-form and already uses FAQ and article schema. What it does not do is tell Google and AI the three things they need before they recommend a law firm: where you are, which named lawyers stand behind the advice, and that independent sources agree. Fix those and the content you are already publishing starts earning citations instead of just traffic.', s1, flags=re.S)
s1 = sub(s1)

# ---------------------------------------------------------------- s2 Your brief
brief_tbl = table(['Question', 'Your answer'], [
    ['Are you interested in engaging a digital growth agency?', PENDB],
    ['Website', 'mycommerciallawyers.com'],
    ['Which service areas do you want to grow?', PENDB],
    ['Are you currently using a marketing agency?', PENDB + ' (your team page lists an in-house SEO specialist and a content creator)'],
    ['Challenges to review on the call', PENDB],
    ['Your position in the firm', PENDB],
])
s2 = section(2, 'Your brief', 'Your brief',
    p('What your site tells us, and what we would confirm with you on the call.')
    + acc('Your answers to our questions', 'To be completed from your enquiry form and our first call', brief_tbl)
    + h3('What we heard')
    + cards([
        ('Disputes only, commercial and construction.', 'That is a strength, not a limitation. Specialist firms do not win by sounding like every other law firm. They win by owning the questions only a specialist can answer, and AI engines reward that even more than Google does.'),
        ('Barrister-led, with litigation solicitors.', 'Authorised by the Bar Standards Board for Direct Public Access and to conduct litigation (reference 191504). Very few firms in your market can say that. Today it lives in the footer.'),
        ('London and Croydon first.', 'You already have Croydon and City of London pages, and your Google profile is #1 in the Maps pack for "construction dispute solicitor london". What is missing is the structure that ties the pages into one London pillar, and an address Google can put on the map.'),
        ('Already publishing.', 'Forty guides, twenty-two of them in 2026, all with article schema. You would start from a body of work, not from nothing. The job is to sign it, connect it and get it cited.'),
        ('Overseas clients are a genuine difference.', 'Pages for international clients, overseas law firms and clients in Oman. Very few UK dispute practices target that. AI answers for "UK dispute lawyer for an overseas company" are where you can lead.'),
    ], cols=5), alt=True)

# ---------------------------------------------------------------- s3 Where MCL is today
service_pages = [
    ('Construction disputes', 'Construction Dispute Solicitors London | Know Your Options', 'Construction'),
    ('Construction contract disputes', 'Construction Contract Solicitors London | Know Your Options', 'Construction'),
    ('Construction adjudication advice', 'Construction Adjudication Solicitors | Check Your Options', 'Construction'),
    ('Construction adjudication UK', 'Construction Adjudication UK | Industry Dispute Resolution', 'Construction (overlaps the page above)'),
    ('Construction litigation', 'Construction Litigation Solicitors | Know Your Options', 'Construction'),
    ('Construction dispute resolution', 'Construction Dispute Resolution Services UK | MCL', 'Construction (overlaps Construction disputes)'),
    ('Construction solicitors', 'No 1 Trusted Construction Solicitors UK: Avoid Disputes', 'Non-contentious construction'),
    ('Unpaid construction invoices', 'Unpaid Construction Invoice Solicitors | Know Your Options', 'Construction payment'),
    ('JCT contract dispute solicitor London', 'JCT Contract Dispute Solicitor in London - My Commercial Lawyers', 'Construction, London'),
    ('Contentious commercial disputes', 'Commercial Dispute Solicitors London | Check Your Options', 'Commercial'),
    ('Breach of contract', 'Breach of Contract Solicitors London | Know Your Options', 'Commercial'),
    ('Debt recovery', 'Commercial Debt Recovery Solicitors | Check Your Options', 'Commercial'),
    ('International arbitration', 'International Arbitration UK | Barrister-Led Dispute Support', 'International'),
]
location_pages = [
    ('Construction solicitor in Croydon', 'Construction Solicitor Croydon | Solicitors & Barristers Support', 'Croydon'),
    ('Commercial lawyer Croydon', 'Commercial Lawyer Croydon | Solicitors & Barristers Support', 'Croydon'),
    ('Construction lawyer City of London', 'Construction Lawyer City of London - My Commercial Lawyers', 'City of London'),
    ('Construction law in London', 'Construction Law London | Know Your Dispute Options', 'London (overlaps four other pages)'),
    ('Construction law firm London', 'Construction Law Firm London: 5 Clear Steps | Commercial Lawyers', 'London (overlaps)'),
    ('Construction solicitor near me', 'Construction Solicitor Near Me for Business Disputes', '"Near me"'),
    ('Commercial lawyer near me', 'Commercial Lawyer Near Me | Solicitor & Barrister Support UK', '"Near me"'),
    ('Breach of contract lawyer near me', 'Breach of Contract Lawyer Near Me | Solicitors Support UK', '"Near me"'),
    ('UK dispute lawyer for international clients', 'UK dispute lawyer for international clients', 'International'),
    ('UK dispute partnerships for overseas law firms', 'UK Dispute Partnerships for Overseas Law Firms', 'International'),
    ('UK dispute lawyer Oman', 'UK Dispute Lawyer Oman - My Commercial Lawyers', 'Oman'),
]
SLUG = {'Construction disputes': '/construction-disputes/', 'Construction contract disputes': '/construction-contract-disputes/', 'Construction adjudication advice': '/construction-adjudication-advice/', 'Construction adjudication UK': '/construction-adjudication-uk/', 'Construction litigation': '/construction-litigation/', 'Construction dispute resolution': '/construction-dispute-resolution/', 'Construction solicitors': '/construction-solicitors/', 'Unpaid construction invoices': '/unpaid-construction-invoices/', 'JCT contract dispute solicitor London': '/jct-contract-dispute-solicitor-london/', 'Contentious commercial disputes': '/contentious-commercial-disputes/', 'Breach of contract': '/breach-of-contract/', 'Debt recovery': '/debt-recovery/', 'International arbitration': '/international-arbitration-uk/',
        'Construction solicitor in Croydon': '/construction-solicitor-in-croydon/', 'Commercial lawyer Croydon': '/commercial-lawyer-croydon/', 'Construction lawyer City of London': '/construction-lawyer-city-of-london/', 'Construction law in London': '/construction-law-in-london/', 'Construction law firm London': '/construction-law-firm-london/', 'Construction solicitor near me': '/construction-solicitor-near-me/', 'Commercial lawyer near me': '/commercial-lawyer-near-me/', 'Breach of contract lawyer near me': '/breach-of-contract-lawyer-near-me/', 'UK dispute lawyer for international clients': '/uk-dispute-lawyer-for-international-clients/', 'UK dispute partnerships for overseas law firms': '/uk-dispute-partnerships-overseas-law-firms/', 'UK dispute lawyer Oman': '/uk-dispute-lawyer-oman/'}
pm1 = table(['Page', 'Page title today', 'Market', 'Keywords / visits'], [[a, b_, c, seo.kv(SLUG[a])] for a, b_, c in service_pages])
pm2 = table(['Page', 'Page title today', 'Market', 'Keywords / visits'], [[a, b_, c, seo.kv(SLUG[a])] for a, b_, c in location_pages])

keyword_fig = seo.keyword_fig()
serp_fig = seo.serp_fig()

findings = (
    finding(1, 'Your address is not where Google and AI look for it',
        'Your homepage contact block and footer give 7 Bell Yard, London WC2A 2JR, and your Google profile already ranks #1 in the Maps pack for "construction dispute solicitor london". But the contact page shows no address, the LegalService schema has no address, phone, hours, geo or area served, and SE Ranking shows the contact page ranking for "7 Savoy Court London WC2R 0EX", which suggests an older address is still attached to you somewhere online.',
        'One verified office address (or a service-area profile), stated identically on the site, in LegalService and LocalBusiness schema and on Google Business Profile, plus areaServed for London, Croydon and the UK.')
    + finding(2, 'Seven pages competing for the same London construction search',
        'Construction disputes, Construction dispute resolution, Construction law in London, Construction law firm London, Construction lawyer City of London, Construction solicitor near me and the JCT London page all target near-identical London construction terms, plus two adjudication pages (Construction adjudication advice and Construction adjudication UK). Google has to guess which one to rank, and usually ranks none of them well.',
        'One London construction disputes hub, with each remaining page owning one distinct question (JCT, adjudication, unpaid invoices, City of London). Merge and redirect the rest.')
    + finding(3, 'Pages that should not be in Google or in front of AI',
        'The thank-you page and an internal "Trello Instructions" page are set to index and listed in your sitemap. A post titled "What are the 5 Cs of food safety: UK business guide" sits among your dispute guides, and two older off-topic posts (criminal-law defences, health and safety penalties) that ranked for 20 keywords now redirect to the homepage, passing those signals to it. One post lives at a broken slug: /construction-disputesknowwhereyoustand/.',
        'Noindex and remove the two utility pages from the sitemap, retire or redirect the off-topic post, and fix the slug with a redirect.')
    + finding(4, 'Schema that says the wrong things',
        'The LegalService schema carries an empty review list and images named "Environmental-and-Safety-Violations" and "Third-Party-Funding". The Organization contact point links to /contact-us/, which redirects to the homepage. Your LinkedIn company page is linked in the header but missing from the schema\'s sameAs list.',
        'Rebuild the entity schema: LegalService with address, phone, hours, areaServed and the BSB reference; Person schema for every barrister and solicitor; sameAs to LinkedIn, the Bar Standards Board register and legal directories.')
    + finding(5, 'No lawyer behind the advice',
        'All 40 guides are signed by "Krystal Blackwell", a WordPress author account with a Gravatar placeholder image and no sameAs links. That name does not appear on your team page. The team page lists 18 people, but every "View Full Profile" link points back to the team page itself.',
        'A profile page for each barrister and solicitor, with call or admission date, regulator, specialism and cases; every guide authored or reviewed by a named lawyer, with a last-reviewed date.')
    + finding(6, 'An AI file that leaves out every page that wins work',
        'Rank Math has generated an llms.txt file, which is good. But it lists only the sitemap and the blog posts. None of your 24 service and location pages appear in it, so the file written for AI assistants describes you as a blog.',
        'Rewrite llms.txt by hand: who you are, who regulates you, where you are, your services and locations first, then the guides.')
    + finding(7, 'Testimonials with nothing behind them',
        'The homepage quotes clients by name, but there is no link to Google reviews or any third-party review platform, and no Review schema. Separately, one service page title says "No 1 Trusted Construction Solicitors UK", a superlative a regulator may ask you to substantiate.',
        'Start a review flow to Google and one legal review platform, mark up genuine reviews, and replace the "No 1" claim with a factual, verifiable one.')
)

mobile = (h3('The mobile test: what a client on a phone actually sees')
    + p('Most people with a dispute look for help on a phone, often outside working hours. We rendered the site on an iPhone-sized screen and ran Google\'s Lighthouse test on the homepage. Four things stand out.')
    + f'''<div class="my-10 space-y-6"><figure class="overflow-hidden rounded-2xl bg-background p-3 ring-1 ring-border sm:p-5"><img src="mobile-test.webp" alt="Three screenshots of mycommerciallawyers.com on a phone: the first screen, the enquiry form and the start of the services section, with problems marked a to d" class="w-full rounded-lg" /><figcaption class="mt-3 text-xs text-muted-foreground">mycommerciallawyers.com on an iPhone-sized screen, {DATE}.</figcaption></figure>'''
    + marked([
        ('A chat bubble sits on the headline', '"Need legal advice? We are available 24/7" covers the line that says what you do.'),
        ('The top-bar phone number cannot be tapped', 'The first tap-to-call link is on screen two.'),
        ('Twenty-one screens long', 'Services ("Our Key Services") do not start until screen six.'),
        ('A long form before any service', 'Seven fields, three of them drop-downs, plus a Trello consent box, ahead of what you actually do.'),
    ], 'Most people look for a dispute lawyer on a phone. This is the first impression they get.') + '</div>')

C = 263.89378290154264
speed = (h3('The speed test: Lighthouse')
    + p('Lighthouse is Google\'s own page-quality test. Scores are out of 100; Google treats anything under 50 as poor. Mobile is the one that matters, because it is the one Google ranks you on.')
    + fig('The speed test: Google Lighthouse on a phone', 'Out of 100. Google treats anything under 50 as poor, and ranks you on the mobile score.',
          '<div class="grid grid-cols-3 gap-6">' + gauge(45, 'Performance') + gauge(87, 'Accessibility') + gauge(79, 'Best practices') + '</div>'
          + '<div class="mt-8 grid gap-3 sm:grid-cols-3">' + darkstat('5.7s', 'before the main content appears', 'Target: under 2.5s') + darkstat('2.1s', 'where taps do nothing', 'Target: under 0.2s') + darkstat('4.1 MB', 'downloaded for one page', 'Target: under 1.5 MB') + '</div>', dark=True)
    + acc('Every speed measure, explained', 'Server response, load time, blocking time, page weight and more', table(['Measure (mobile)', SHORT, "Google's target", 'What it means'], [
        ['Performance score', '45 / 100', '90+', 'Poor. The page is slow to become usable on a phone.'],
        ['Server response time', '0.12 seconds', 'Under 0.6 s', 'Good. The caching works; the problem is what the page then loads.'],
        ['Largest content paint', '5.7 seconds', 'Under 2.5 s', 'The main content takes nearly six seconds to appear.'],
        ['Total blocking time', '2.1 seconds', 'Under 0.2 s', 'Over two seconds where taps do nothing. 349 KB of unused JavaScript is loading.'],
        ['Page weight', '4.1 MB', 'Under 1.5 MB', 'Images in old formats: 1.8 MB could be saved by converting them alone.'],
        ['Accessibility', '87 / 100', '90+', 'Contrast failures, form fields and drop-downs without labels, headings out of order.'],
        ['Best practices', '79 / 100', '90+', 'Third-party cookies and browser issues logged on load.'],
        ['SEO (technical)', '100 / 100', '90+', 'The basics pass. This score does not measure location, authorship or entity signals, which is where the real gap is.'],
    ]) + h4('Mobile speed against the firms ranking for your London searches') + table(['Firm', 'Score', 'Details'], [['Osbornes Law (organic #2)', '100', '(server response 0.26s, largest content paint 1.1s)'], ['B P Collins (organic #4)', '39', '(server response 0.25s, largest content paint 4.2s)'], [FIRM, '45', '(server response 0.12s, largest content paint 5.7s)']]))
    + quote(b('Why this matters for the plan.') + ' Every speed problem above comes from the same place: an Elementor and Pro Elements build on the Astra theme, loading 4 MB of scripts and uncompressed images. Patching it costs nearly as much as rebuilding it. That is why Section 8 includes a new AI-ready site at no cost.'))

s3 = section(3, 'Where MCL is today', f'Where {SHORT} is today',
    p(f'Every page on the site, what it is built to win, and how it performs on a phone. Sources: a live crawl of all 75 URLs in your sitemap, Lighthouse 12 and a mobile render of the homepage on {DATE}. Rankings and traffic: SE Ranking, Google UK database, pulled 13 October 2026.')
    + stats([('365', 'keywords ranking anywhere in Google\'s top 100'), ('94', 'of those in the top 10'), ('195', 'estimated organic visits a month, worth about $1.2K in ads'), ('190', 'of those 195 visits land on the homepage; your service pages earn none')])
    + keyword_fig
    + p('Three hundred and sixty-five keywords sounds healthy until you look at which pages they sit on. 268 of them belong to the homepage, which ranks #1 for broad terms such as "commercial law firm" (590 searches a month) and "commercial lawyers" (320), but also for other firms\' names and lookalikes ("my solicitors", "mc solicitors", "mcleods barristers and solicitors") because your name begins with "My". Your seven service and location pages that rank at all hold 30 keywords between them and bring in no measurable visits. The technical basics are sound: every page has a single H1, a title, a meta description, and the service pages carry FAQ schema across all 75 URLs we crawled.')
    + h3('The page map')
    + p('Thirty-five pages and forty guides are in your sitemap. Here is every page built to win work, what its title says today, the market it targets, and what SE Ranking says it ranks for (keywords in the top 100 / estimated visits a month).')
    + acc('Service pages', 'Thirteen practice-area pages, three of which overlap', pm1)
    + acc('Location and audience pages', 'Croydon, City of London, "near me" and international', pm2)
    + plain('your service pages, the pages that should be winning clients, are almost invisible. Seventeen of the twenty-four rank for nothing at all. The homepage is doing all the work, and it is doing it for broad commercial terms, not for construction disputes, which is your strongest practice.')
    + h3('The London test')
    + p('We looked at the searches a business owner in London would type, using the results pages SE Ranking stored on 13 October 2026 (Google UK; SE Ranking offers no London-only location). Your Google profile wins the map. Your website does not appear on page one for any of them.')
    + serp_fig
    + acc('All four London searches in full', 'construction dispute solicitor london, commercial litigation solicitor london, commercial lawyer london, construction solicitor croydon', seo.serp_table())
    + h3('Three things the London results tell us')
    + cards([
        ('You already win the map.', 'Your Google profile is #1 in the Maps pack for "construction dispute solicitor london" and #3 for "commercial litigation solicitor london", ahead of Fenwick Elliott. That is the hardest slot to take, and you hold it.'),
        ('Page one is won by one good page.', 'Osbornes Law, B P Collins, Forsters and Russell-Cooke each rank with a single, dedicated construction disputes page. Your /construction-disputes/ page ranks #81 for "construction dispute". The structure works; your page is not built for it yet.'),
        ('Legal 500 is on page one for both searches.', 'And it is cited in the AI answers in your topics. A directory listing is the shortest route onto page one and into AI answers for a firm with domain trust of 10.'),
    ])
    + h3('Why the site isn\'t ranking as it should')
    + p('Seven findings from the crawl, in the order we would fix them. None of them is a criticism of the firm. They are the gap between a site built to describe a business and a site built to be found and cited.')
    + findings + mobile + speed)

# ---------------------------------------------------------------- s4 E-E-A-T
eeat = L(1852, 1898)  # E-E-A-T explainer block from the template
eeat = eeat.replace('Family law is what Google calls', 'Commercial dispute advice is what Google calls')
s4_intro = p('Legal advice on disputes is what Google calls a "Your Money or Your Life" topic: advice that can change a business\'s finances or survival. For those topics Google and the AI assistants apply their strictest test of who wrote a page and whether they can be believed. Google calls it E-E-A-T.')
eeat_cards = cards([
    ('Experience', 'Has the author actually done this? First-hand detail only a practising barrister or solicitor would know. Adjudication guides written from the practice, not paraphrased from the TCC guide.'),
    ('Expertise', 'Is the author qualified to say it? A named barrister or solicitor on every page of advice, with call or admission date, regulator and specialism, linked to a profile that proves it.'),
    ('Authoritativeness', 'Do others recognise them for it? Chambers listings, the Bar Standards Board register, the Law Society, legal directories, press and other sites that say the same thing about the same person.'),
    ('Trust', 'Can the reader rely on this page today? Dates, a reviewer, working links, consistent facts, reviews, a real address and phone, a secure fast site. Trust is the one Google says matters most.'),
], cols=4)
blog_tbl = table(['Finding', 'Detail', 'Why it matters'], [
    ['Fresh', 'Twenty-two of forty guides were published in 2026, most of them updated in August and September.', 'A strength. Google and AI weight freshness heavily on legal topics. Keep the cadence.'],
    ['Unsigned by a lawyer', 'All forty guides carry the same author account, "Krystal Blackwell", who has no profile, role or credentials on the site.', 'Advice from an unverifiable author on a legal site is a negative signal under the quality guidelines.'],
    ['Off-topic', '"What are the 5 Cs of food safety: UK business guide" sits among the dispute guides.', 'It tells Google and AI the site is a general business blog, diluting the specialism.'],
    ['Overlapping', 'Guides such as "London construction lawyer: what to check first", "How to choose a construction dispute solicitor in London" and "The contract is not clear" (London) chase the same searches as your London service pages.', 'They compete with each other and with your own service pages for the same searches.'],
    ['A thinner 2025 batch', 'Most of the eighteen guides from September to November 2025 are short, news-style pieces of about a thousand words (Building Safety Levy, Arbitration Act 2025, late payment).', 'Good topics that need a lawyer\'s byline, a review date and links into the service pages to earn their keep.'],
    ['Good bones', 'The 2026 guides (adjudication checks, JCT contracts, claim versus dispute, debt recovery versus dispute) are substantial and well structured.', 'These are the easiest wins on the site: sign, review-date, link into the pillars.'],
])
s4 = section(4, 'Why Google and AI do not trust the site yet', 'Why Google and AI do not trust the site yet',
    s4_intro + h3('E-E-A-T in one minute') + eeat_cards
    + p('AI assistants work the same way. When ChatGPT or Google AI decide whether to name a firm, they look for a person, credentials they can verify elsewhere, and content that is current and corroborated. Section 6 shows what that means for you.')
    + h3('What the site tells them about your lawyers')
    + p('Your credentials are genuinely strong: barristers authorised by the Bar Standards Board for Direct Public Access and to conduct litigation, alongside litigation and construction solicitors. Almost none of it is in a form Google or AI can read. Here is what they find instead.')
    + acc('1. Eighteen names, no profiles', 'What it signals: no verifiable lawyer behind any page.',
          p(b('What we found:') + ' The team page lists eighteen people, from regulatory barristers to receptionists, in 316 words including navigation. Every "View Full Profile" link points back to /team/.') + p(b('What it signals:') + ' There is no profile page for any barrister or solicitor, and no Person schema, so no byline can resolve to a real lawyer.'))
    + acc('2. The regulator is only in the footer', 'What it signals: the strongest trust fact on the site is the hardest to find.',
          p(b('What we found:') + ' "Authorised and regulated by the Bar Standards Board ... reference no: 191504" appears once, in the footer, and in no schema.') + p(b('What it signals:') + ' AI cannot connect you to the BSB register, so it cannot confirm you are a regulated legal practice rather than a lead-generation site.'))
    + acc('3. Every guide signed by a name Google cannot place', 'What it signals: Google sees "Krystal Blackwell" as text, not as a lawyer.',
          p(b('What we found:') + ' The BlogPosting schema names Krystal Blackwell as author and editor, linked to a WordPress author archive with a placeholder image and no sameAs links.') + p(b('What it signals:') + ' The byline carries no weight, and on a YMYL topic it can count against you.'))
    + h3('The blog: forty guides, twenty-two of them from 2026')
    + acc('Six findings from the blog', 'Fresh, unsigned, off-topic, overlapping, a thin 2025 batch, and good bones', blog_tbl)
    + quote(b('What we do about it.') + ' A proper profile page for each barrister and solicitor with Person schema linked to the Bar Standards Board or Law Society register, LinkedIn and legal directories, so every byline resolves to a verifiable lawyer. Every guide gets a named lawyer as author or reviewer, a last-reviewed date and Article schema. The forty guides are triaged: sign the strong 2026 ones, merge the overlapping London construction guides, retire the off-topic post, and link every guide into its service pillar. This is part of the Fix step in month one, and it is re-checked every month after.'), alt=True)

# ---------------------------------------------------------------- s5 Competitors (pending SE Ranking)
maps_fig = fig('The Maps pack today', 'Google UK, stored by SE Ranking on 13 October 2026.', seo.maps_tbl())
s5 = section(5, 'Who you are up against in London', 'How you compare with the firms on London page one',
    p('Same tool, same month, same country. Keyword counts, traffic and links are SE Ranking estimates for the Google UK database, pulled 13 October 2026.')
    + acc('Who SE Ranking thinks you compete with', 'Its ten closest organic competitors, mostly name lookalikes', seo.competitors_tbl())
    + p('<em class="text-sm text-muted-foreground not-italic">Top 10 is n/a for competitors because SE Ranking shows their top-10 share only as a percentage. Five of the ten share your "My..." naming pattern rather than your practice: Google is grouping you by name, not by construction disputes. Your real competitors are the firms below.</em>')
    + seo.traffic_fig()
    + h3('Who is actually on London page one')
    + acc('The firms a London contractor sees', 'From the stored results pages for your London searches', seo.page_one_tbl())
    + h3('The Maps pack is a review contest, and you are already in it')
    + p('The three firms Google shows on the map are chosen on relevance, distance and prominence, and prominence is mostly reviews. You hold #1 for "construction dispute solicitor london" and #3 for "commercial litigation solicitor london", but you are not in the pack for "commercial lawyer london". SE Ranking does not show review counts for Maps entries, so we record yours and your rivals\' from Google Maps in week one. Your site does not link to the profile or show its reviews.')
    + maps_fig
    + h3('What nobody in London is likely to do, which is where you win')
    + cards([
        ('Barrister-led Direct Public Access.', 'A business can instruct a barrister directly, without a solicitor in between. That is a cost and speed story most dispute firms cannot tell, and AI answers to "how much does a construction dispute cost" can carry it.'),
        ('Scope and fee before work begins.', 'Your homepage already says "Know the scope and fee before work begins". Few firms publish a fee answer for adjudication or debt recovery. A firm that does can own the cost question.'),
        ('Overseas clients.', 'Pages for overseas law firms, international clients and clients in Oman. "UK dispute lawyer for an overseas company" is a question AI is asked, and few UK firms answer it directly.'),
        ('Seven days a week.', 'Office hours of 6am to 10pm every day are listed on the contact page. Disputes do not wait for Monday; say it where the client decides.'),
        ('Construction and commercial under one roof.', 'Adjudication, JCT disputes, unpaid invoices, breach of contract and debt recovery. A hub that links them answers the whole question a contractor has, not one part of it.'),
    ]))

# ---------------------------------------------------------------- s6 What AI says about you
from s6 import build as build_s6
s6 = build_s6(DATE)

# ---------------------------------------------------------------- s7 Action plan
inventory = table(['Group', 'What you offer today', 'Where it lives'], [
    ['Construction disputes', 'Construction disputes; construction contract disputes; JCT, FIDIC and NEC disputes; construction litigation; dispute resolution', 'Five service pages, one JCT London page'],
    ['Adjudication', 'Construction adjudication advice; adjudication in the UK; enforcing an adjudicator\'s decision in the TCC (guide)', 'Two overlapping service pages, several guides'],
    ['Payment', 'Unpaid construction invoices; retention disputes; late payment; letters before action', 'One service page, four guides'],
    ['Commercial disputes', 'Contentious commercial disputes; breach of contract; business-to-business disputes', 'Two service pages, one "near me" page, many guides'],
    ['Debt recovery', 'Business debt recovery; fixed-fee debt recovery', 'One service page, three guides'],
    ['International', 'International arbitration; overseas clients; overseas law firm partnerships; Oman', 'Four pages'],
    ['Non-contentious', 'Construction solicitors (avoiding disputes)', 'One page; title needs a factual rewrite'],
])
kw = seo.kw_service()
pillar = fig('How a location pillar works', 'One hub, five supporting pages, the service pillars feeding in, and a trust layer that proves it all to Google and AI.',
    '<p class="mb-2 text-center text-xs font-bold tracking-widest text-muted-foreground uppercase">Service pillars (national)</p>'
    + chips('bg-surface ring-1 ring-border', ['Construction disputes', 'Adjudication', 'Unpaid invoices and debt recovery', 'Commercial and breach of contract'])
    + ARROW_D + f'<div class="mx-auto max-w-md rounded-2xl bg-primary px-6 py-6 text-center text-primary-foreground shadow-lg"><p class="text-xs font-bold tracking-widest text-accent uppercase">Location hub</p><p class="mt-1 font-display text-2xl font-bold">Construction dispute solicitor London</p><p class="mt-1 text-xs text-primary-foreground/65">Maps #1 today · \"construction dispute lawyer\" 210 searches a month, difficulty 15</p></div>' + ARROW_D
    + '<p class="mb-2 text-center text-xs font-bold tracking-widest text-muted-foreground uppercase">Supporting pages: each owns one London question</p>'
    + chips('bg-accent/25 ring-1 ring-accent', ['JCT contract disputes in London', 'Adjudication in London and the TCC', 'Unpaid invoices for London contractors', 'Construction disputes in the City', 'Construction solicitor Croydon'])
    + ARROW_D + '<p class="mb-2 text-center text-xs font-bold tracking-widest text-muted-foreground uppercase">Trust layer: what corroborates every claim</p>'
    + chips('bg-secondary/10 ring-1 ring-secondary/30', ['Google profile and reviews', 'Barrister and solicitor profiles and schema', 'BSB register and legal directories', 'Thought leadership in construction and legal press', 'Same name, address, phone, hours']))
pillar_tbl = table(['Layer', 'Page', 'Target', 'What it contains'], [
    ['Hub', '/construction-dispute-solicitor-london/', 'construction dispute solicitor london, construction lawyer london', 'Who you are in London, the barrister-led Direct Public Access model, every construction service, scope and fee before work begins, lawyer profiles, reviews, map, FAQs, links to every supporting page. Replaces the overlapping London pages.'],
    ['Support', '/london/jct-contract-disputes/', 'jct contract dispute solicitor london', 'The existing JCT London page, focused on one question.'],
    ['Support', '/london/construction-adjudication/', 'construction adjudication london', 'How adjudication works for London projects, the TCC, enforcement, timescales, fees.'],
    ['Support', '/london/unpaid-construction-invoices/', 'unpaid invoice solicitor london', 'Payment notices, pay less notices, retention, what to do this week.'],
    ['Support', '/construction-lawyer-city-of-london/', 'construction lawyer city of london', 'The existing page, linked into the hub.'],
    ['Support', '/construction-solicitor-in-croydon/', 'construction solicitor croydon', 'The existing Croydon page, linked into the hub, with the Croydon cost guide.'],
    ['Trust', 'Google Business Profile', 'Maps pack for London and Croydon searches', 'A verified profile at a real address, services completed, photos, posts, and a review flow that names the service.'],
    ['Trust', 'Citations and press', 'AI corroboration', 'Bar Standards Board register, Law Society Find a Solicitor, The Legal 500, Chambers, Construction News, Building, local business directories.'],
])
authority = table(['Signal', 'What we build', 'Where it works'], [
    ['The expert', 'A full profile for each barrister and solicitor: call or admission date, regulator, specialism, notable matters, Person schema, and their name on every guide they write or review.', 'Google E-E-A-T, AI answers that name a lawyer, the "best construction solicitor" queries'],
    ['The entity', 'LegalService and LocalBusiness schema with one address, identical name, address, phone and hours on the site, Google, LinkedIn and every directory, plus the BSB reference.', 'Maps pack, Google AI Mode, ChatGPT and Perplexity citations'],
    ['Information gain', 'Pages that say something not already on page one: what an adjudication really costs, a pay less notice checklist, how Direct Public Access works for a business.', 'AI quotes the page that adds something new. This is how Deen &amp; Co went from zero to 29% of ChatGPT answers.'],
    ['Social proof', 'A review flow after every matter, naming the service and the area, on Google and one legal review platform.', 'Maps prominence, review snippets, "best" queries'],
    ['Third-party corroboration', 'UK legal directories, construction trade press, the Bar Standards Board and Law Society registers, LinkedIn.', 'Referring domains that are UK and legal'],
    ['The track record', 'Every guide signed or reviewed by a named lawyer with a last-reviewed date and Article schema; overlapping guides merged; case studies linked to the services.', 'The E-E-A-T gap closed: Google and AI can connect the byline to the lawyer.'],
    ['Technical trust', 'Fast on mobile, labelled forms, no indexed utility pages, a hand-written llms.txt, FAQ schema on every guide.', 'Rankings, and the Lighthouse scores in Section 3 turning green'],
])
three = ('<div class="my-10 grid gap-4 lg:grid-cols-3">'
    + slot(PIN('h-6 w-6 text-secondary'), 'Win the maps', 'Maps #1 for construction, #3 for commercial litigation, absent for commercial lawyer london', ['A verified profile at a real address', 'Reviews that name the service', 'Same details on every directory'])
    + slot(SEARCHBIG, 'Win the organic', 'Website not in the top 100 for construction dispute solicitor london', ['One London hub plus five supporting pages', 'Overlapping pages merged and redirected', 'A fast new site'])
    + slot(SPARK('h-6 w-6 text-secondary'), 'Win the AI answer', 'Six firms cited in the AI Overview, not you', ['Teach AI where you are', 'Barrister and solicitor profiles', 'UK legal citations and press'])
    + '</div>')
s7 = section(7, 'The action plan', 'The action plan',
    p('Everything you do, the keywords for each of those services, the local terms on top, and the structure that turns both into authority. Search volumes and difficulty are SE Ranking, Google UK, October 2026; difficulty is 0 to 100, and anything under 20 is winnable within a few months for a well-built page.')
    + h3('7.1 Everything you do: the service inventory')
    + p('Before any keyword research we listed every service on the site, because each one is a question somebody types into Google or asks an AI.')
    + acc('The full service inventory', 'Construction, adjudication, payment, commercial, debt recovery, international', inventory)
    + plain('you already have more service and location pages than you need. The plan is not more pages. It is fewer, clearer ones, each owning one question, each signed by a lawyer.')
    + h3('7.2 Keyword research: the questions behind each service')
    + p('For every service above we found what businesses in the UK actually search. Difficulty under 20 means a well-written page from a credible firm can rank within months. Almost every term below is under 20, and your existing pages compete for none of them from page one.')
    + acc('Keywords for every service', 'Construction, adjudication, payment, commercial, debt, international', kw)
    + h3('7.3 Keyword research: the local layer')
    + p('Service pages answer the question. Local pages answer "near me". London first, then Croydon, then the overseas audience you already serve.')
    + acc('London (your first pillar)', 'construction lawyer london, construction solicitor london, commercial litigation solicitor london', seo.kw_london())
    + acc('Croydon', 'Your existing Croydon pages and two Croydon guides', seo.kw_croydon())
    + p('<em class="text-sm text-muted-foreground not-italic">"Not in UK database" means the search is too small for SE Ranking to track in its UK database. Croydon and the City of London are still worth a page each (they convert, and AI answers name a firm for them); we track them in a rank-tracking project from month one rather than guess a volume.</em>')
    + h3('Already ranking: quick wins we would take in month one')
    + acc('Eight searches one step off page one, or just on it', 'All currently held by the homepage; each moves to the page built for it', seo.quick_wins())
    + h3('7.4 The pillar structure, explained')
    + p('A pillar is not one "London" page with the area name swapped in. It is a hub page plus a set of supporting pages that each own one question, all linking back to the hub, and all corroborated by a trust layer outside the site. Google and AI then see one firm that answers everything about construction disputes for businesses in London, rather than seven pages that mention it.')
    + pillar + acc('Every page in the London pillar', 'Hub, five supporting pages and the trust layer', pillar_tbl)
    + quote(b('A note on the office address.') + ' Your homepage and footer give 7 Bell Yard, London WC2A 2JR, your Google profile already ranks in the Maps pack, and SE Ranking still connects your contact page to "7 Savoy Court London WC2R 0EX". We confirm which address the profile uses and make every listing match it. Google requires a Business Profile address to be somewhere clients can meet you, at least by appointment. If that is true of the Bell Yard address, everything above is straightforward. If not, we set the profile up as a service-area business for London and the South East, which still gets you into the map results.')
    + h3('7.5 How we make you the authority')
    + p('Google and AI do not rank firms, they rank evidence. Authority is a set of signals that all say the same thing about the same people, in the same words, in places the firm does not control. Here is what we build for ' + FIRM + ' and where each piece shows up.')
    + acc('The seven authority signals we build', 'Expert, entity, information gain, reviews, citations, track record, technical trust', authority)
    + h3('7.6 How you dominate London')
    + p('Page one for "construction dispute solicitor london" has three places a client can tap before they scroll: the Maps pack, the organic results and the AI answer. The plan is built to hold all three.')
    + three + p('Then the same three-slot play is repeated for Croydon, then for the national adjudication and debt recovery searches, using the same hub-and-spoke structure and the same trust layer.'))

# ---------------------------------------------------------------- s8 Method (template, adapted)
s8 = L(4107, 4434)
gantt = [('New site, built free', 0, 33.33), ('London construction pillar', 0, 100), ('Service pillars', 0, 100), ('Croydon, then national', 0, 100),
         ('Google Business Profile and Maps pack domination', 0, 100), ('Fee and dispute tools', 16.67, 83.33), ('Authoritative content build', 16.67, 83.33), ('Build the buzz: citations, press and backlinks', 16.67, 83.33)]
gi = iter(gantt)
def gfix(m):
    name, left, width = next(gi)
    return m.group(0)
s8 = s8.replace('the Ballarat court guide, the real cost of family law in Victoria. Reviewed by Emma.', 'what adjudication really costs, a pay less notice checklist. Reviewed by your barristers.')
for a, b_ in [('>Ballarat pillar<', '>London construction pillar<'), ('>Melbourne, Geelong, Bendigo and statewide<', '>Croydon, then national<'), ('>Family law tools<', '>Fee and dispute tools<')]:
    s8 = s8.replace(a, b_)
# animated bars: give them their final positions
rows = re.findall(r'style="left: ([0-9.]+)%; width: 0%; transition-delay: (\d+)ms"', s8)
widths = [33.33, 100, 100, 100, 100, 83.33, 83.33, 83.33]
for (left, delay), w in zip(rows, widths):
    s8 = s8.replace(f'style="left: {left}%; width: 0%; transition-delay: {delay}ms"', f'style="left: {left}%; width: {w}%"', 1)
s8 = s8.replace('flex items-center overflow-hidden whitespace-nowrap rounded-md px-3 text-xs font-bold transition-all duration-700 ease-out bg-accent text-accent-foreground"\n                        style="left: 0%; width: 33.33%"\n                      ></div>',
                'flex items-center overflow-hidden whitespace-nowrap rounded-md px-3 text-xs font-bold transition-all duration-700 ease-out bg-accent text-accent-foreground"\n                        style="left: 0%; width: 33.33%"\n                      >Months 1 to 2</div>')
s8 = re.sub(r'Section 3 showed a site that takes two seconds to respond.*?and we do not charge for\s+it\.',
            'Section 3 showed a homepage that downloads 4 MB, takes almost six seconds to show its main content on a phone, hides its services until screen six and cannot be called with a tap from the top bar. Fixing that build piece by piece costs almost as much as replacing it, and leaves you with Elementor underneath. So with buzzExpansion and buzzInfluence we build My Commercial Lawyers a new site, and we do not charge for it.', s8, flags=re.S)
s8 = s8.replace('LegalService, LocalBusiness (both offices), Attorney (Emma), Service and Offer (your fixed\n                  prices), FAQPage, Review.', 'LegalService, LocalBusiness, Person for every barrister and solicitor, Service and Offer (your fixed fees), FAQPage, Review, and the BSB reference.')
s8 = s8.replace('one\n                  navigation instead of four.', 'one\n                  light theme instead of a page builder.')
s8 = s8.replace("Name, both addresses, phone, hours, Emma's credentials and your prices stated once,\n                  consistently, in text AI can quote. The subscription story told plainly.", 'Name, address, phone, hours, each lawyer\'s credentials, the regulator and your fee approach stated once, consistently, in text AI can quote. The Direct Public Access story told plainly.')
s8 = s8.replace('Tap-to-call and Book a free 15-minute consult in the header on every page, services on the first screen,\n                  pricing visible without a form, the booking tool without a second cookie banner.', 'Tap-to-call and "Check your dispute options" in the header on every page, services on the first screen, a three-field form instead of seven, nothing covering the headline.')
s8 = s8.replace('so the affidavit and court fees posts keep what they have.\n                  Product pages folded into the services.', 'so the guides keep what they have.\n                  Overlapping pages merged into the pillars.')
s8 = s8.replace("Emma's review time.", "Your lawyers' review time.")
s8 = s8.replace("Everything we write follows the Australian\n                  Solicitors' Conduct Rules and the Victorian Legal Services Board and Commissioner's advertising guidance", 'Everything we write follows the BSB Handbook and the SRA\'s rules on publicity')
s8 = s8.replace('<strong class="font-semibold text-foreground">One decision on price.</strong> Which subscription figure is right, and whether the price list can live on the page.', '<strong class="font-semibold text-foreground">One decision on fees.</strong> Which services can carry a published fee or fee range, so the cost question has an answer on the page.')
s8 = s8.replace('- Page-one keywords in Ballarat, Melbourne and nationally - Map pack appearances for "family lawyer ballarat" - Pages cited by Google AI and ChatGPT', '- Page-one keywords in London, Croydon and nationally - Map pack appearances for London and Croydon searches - Pages cited by Google AI and ChatGPT')
s8 = s8.replace('- Share of AI answers naming Anchored (from 1.3%) - Google reviews in Ballarat (from 2) - Australian legal citations and press earned', '- Share of AI answers naming My Commercial Lawyers (from 0.01%, named in 0 answers) - Google reviews (baseline to confirm) - UK legal citations and press earned')
s8 = s8.replace('- Enquiries and free consults by location and service', '- Enquiries and consultations by location and service')
s8 = s8.replace('consults by location and service, calls from Maps', 'consultations by location and service, calls from Maps')
s8 = sub(s8)

# ---------------------------------------------------------------- s9 Sales (template, adapted)
s9 = L(4435, 4764)
s9 = s9.replace('a 30-minute sales process analysis with Emma', 'a 30-minute sales process analysis with your team')
s9 = s9.replace('People looking for a family lawyer are stressed', 'Business owners with a dispute are stressed')
s9 = s9.replace('Family law tone', 'Dispute tone').replace('Empathy, confidentiality and one clear first step', 'Calm, commercial and one clear first step')
s9 = s9.replace('"I need to talk to my partner"', '"I need to talk to my business partner"')
s9 = sub(s9)

# ---------------------------------------------------------------- s10 Working together (template, GBP to confirm)
s10 = L(4765, 5387)
P = lambda: pending('£ to confirm')
s10 = s10.replace('Google Business Profile and the Maps pack · A$1,235.42 a month', 'Google Business Profile and the Maps pack · ' + P() + ' a month')
s10 = s10.replace('Own Ballarat, then Victoria · A$3,000 a month', 'Own London construction disputes, then national · ' + P() + ' a month')
s10 = s10.replace('Own the online family law position · A$5,000 a month, depending on scope', 'Own the AI answer for UK construction and commercial disputes · ' + P() + ' a month, depending on scope')
s10 = s10.replace('Ballarat Google Business Profile completed, verified and optimised', 'Google Business Profile completed, verified and optimised')
s10 = s10.replace('For: winning the Ballarat Maps pack first.', 'For: winning the London and Croydon Maps pack first.')
s10 = s10.replace('Target 20 to 30 keywords: the Ballarat pillar, service pillars, then Melbourne, Geelong and Bendigo', 'Target 20 to 30 keywords: the London construction pillar, the service pillars, then Croydon and national')
s10 = s10.replace('For: the regional presence in your brief, built properly.', 'For: the London presence your site is reaching for, built properly.')
s10 = s10.replace('including fixed fee, subscription and unbundled', 'including adjudication, debt recovery and overseas clients')
s10 = s10.replace('For: becoming the firm AI names for fixed-fee family law anywhere in Australia.', 'For: becoming the firm AI names for construction and commercial disputes anywhere in the UK, and for overseas clients.')
s10 = s10.replace('A$1 when we build your new site, or 50% off when you keep and optimise your current one.', '£1 when we build your new site, or 50% off when you keep and optimise your current one.')
s10 = s10.replace('<td class="border-t border-border px-4 py-3 align-top leading-snug">A$1,235.42</td>', f'<td class="border-t border-border px-4 py-3 align-top leading-snug">{P()}</td>')
s10 = s10.replace('A$617.71 (50% off)', '50% off').replace('<td class="border-t border-border px-4 py-3 align-top leading-snug">A$3,000</td>', f'<td class="border-t border-border px-4 py-3 align-top leading-snug">{P()}</td>')
s10 = s10.replace('A$5,000, depending on scope', P() + ', depending on scope').replace('>A$1<', '>£1<').replace('A$1,500 (50% off)', '50% off').replace('A$2,500 (50% off)', '50% off')
s10 = re.sub(r'<p class="my-4 max-w-3xl leading-relaxed text-foreground/85">\s*<strong class="font-semibold text-foreground">Like what you hear\?.*?</p>', p(b('Like what you hear?') + ' A sign-up-today rate for buzzExpansion ' + P() + ', still with the £1 first month or 50% off, for 48 hours.'), s10, flags=re.S)
s10 = s10.replace('the Ballarat profile is completed, the review flow starts, and\n              the new site is in design with Emma.', 'the Google profile and address are settled, the review flow starts, and\n              the new site is in design with your team.')
s10 = s10.replace('The new site goes live with the Ballarat hub', 'The new site goes live with the London hub')
s10 = sub(s10)

# ---------------------------------------------------------------- closing band
close = L(5388, 5414)
close = close.replace("Let's get Anchored Family Law found first in Ballarat.", "Let's get My Commercial Lawyers found first in London.")
close = close.replace('legalbuzz for Emma Maxwell, Anchored Family Law', 'legalbuzz for the My Commercial Lawyers team')
close = close.replace('href="/book-a-call"', 'href="https://legalbuzz.co/book-a-call"')
close = close.replace('<section id="s11"', '<!--s11-->')  # guard
close = close.split('<!--s11-->')[0]

# ---------------------------------------------------------------- s11 case studies (template facts, prospect-specific "why it matters")
s11 = L(5415, 5642)
s11 = s11.replace('The closest situation to yours.', 'A familiar starting point.')
s11 = s11.replace('<strong class="font-semibold text-foreground">Why it matters for Anchored.</strong> Same starting point: a decent-looking site that said nothing a client types. The location pages did\n                the work, exactly as the Ballarat pillar is designed to.',
                  '<strong class="font-semibold text-foreground">Why it matters for My Commercial Lawyers.</strong> A decent-looking site that was not being chosen. Clear location pages, schema and a rebuilt Google profile did the work, exactly as the London pillar is designed to.')
s11 = re.sub(r'<strong class="font-semibold text-foreground">Why it matters for Anchored\.</strong> A specialist with a clear niche.*?has published it\.',
             '<strong class="font-semibold text-foreground">Why it matters for My Commercial Lawyers.</strong> A London specialist with a clear niche beat bigger firms by answering the exact question people ask, when they ask it. Your version of that question is cost and next step: "how much does adjudication cost", "what to do about an unpaid construction invoice". Your guides already answer it. They need a lawyer\'s name on them.', s11, flags=re.S)
s11 = re.sub(r'<strong class="font-semibold text-foreground">Why it matters for Anchored\.</strong> The closest practice area\..*?than Essex\.',
             '<strong class="font-semibold text-foreground">Why it matters for My Commercial Lawyers.</strong> A specialist firm with strong lawyers and little verifiable footprint online, fixed with service pillars plus town pages. The same structure works for London and Croydon.', s11, flags=re.S)
s11 = re.sub(r'<strong class="font-semibold text-foreground">Why it matters for Anchored\.</strong> The pillar model at scale.*?at your size\.',
             '<strong class="font-semibold text-foreground">Why it matters for My Commercial Lawyers.</strong> The pillar model at scale: half of what the site earns comes from pages that name a place. London, then Croydon, then national, is the same model at your size.', s11, flags=re.S)
s11 = s11.replace('In summary: what we did, what they do, what the Ballarat firms do', 'In summary: what we did, and what changes for My Commercial Lawyers')
s11 = s11.replace('The clients above, the Ballarat firms, and Anchored after this plan', 'The clients above, and My Commercial Lawyers after this plan')
s11 = s11.split('<h3 class="mt-12 mb-4 font-display text-2xl font-bold lg:text-3xl">In summary')[0]
summary = acc('The side-by-side summary', 'The clients above, and My Commercial Lawyers today and after this plan', table(['', 'The clients above', f'{SHORT} today (verified {DATE})', f'{SHORT}, after this plan'], [
    ['The site', 'Rebuilt or fixed first: fast, readable by AI, schema on every page', 'Elementor build, Lighthouse 45 on mobile, 4 MB homepage; good FAQ and article schema', 'New AI-ready site at no cost, Lighthouse 90+, entity and Person schema throughout'],
    ['Location', 'A page for every town served, linked into a hub', 'Croydon, City and "near me" pages; 190 of 195 visits on the homepage; seven pages splitting London', 'London hub plus five supporting pages, then Croydon and national'],
    ['Services', 'A pillar per practice area answering what clients type', 'Thirteen service pages, three overlapping', 'Five service pillars, each owning its questions'],
    ['Trust', 'Named authors, reviews built steadily, citations and press', 'One unverified author on 40 guides; testimonials with no platform; BSB status in the footer only', 'Named barristers and solicitors as authors, a review engine, BSB reference in schema, UK legal citations'],
    ['AI', "Tracked monthly; J Scott named 687 times, Deen &amp; Co 7,017 citations", '0.01% AI presence; cited in 27 answers, named in none; llms.txt lists no service pages', 'Share of voice tracked monthly against the London firms, from 0.01% upward'],
    ['Measured on', 'Enquiries: 15 to 77, 33 in a month, +300%', '195 Google visits a month today; enquiry baseline recorded in week 1', 'Enquiries and consultations, by location and service, every month'],
]))
s11 += h3('In summary: what we did, and what changes for My Commercial Lawyers') + summary
s11 += h3('Your current Google rankings') + p('Every keyword ' + FIRM + ' ranks for in Google UK\'s top 10, grouped by the page that ranks. Source: SE Ranking, Google UK database, 13 October 2026. Searches are monthly averages.')
s11 += seo.rankings_acc() + p('<em class="text-sm text-muted-foreground not-italic">Not one of your 94 top-10 rankings contains "adjudication", "Croydon" or "City of London", and only 5 contain "construction", your core practice.</em>')
s11 += '</div></section></div>'

# ---------------------------------------------------------------- footer (template, verbatim)
foot = L(5985, len(TPL))
foot = re.sub(r'(href|src)="/(?!/)', r'\1="https://legalbuzz.co/', foot)
foot = re.sub(r'<script\b.*?</script>', '', foot, flags=re.S)
foot = foot.replace('https://legalbuzz.co/assets/george-profile-IpPg1vSs.jpeg', 'assets/george-profile-IpPg1vSs.jpeg').replace('https://legalbuzz.co/__l5e/assets-v1/608bd5cd-19bb-40da-af9f-f532979db9ea/pj-singh.jpg', 'assets/pj-singh.jpg').replace('loading="lazy"', '')

page = '\n'.join([head, hero, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, close, s11, foot])
page = page.replace('aria-expanded="false"', 'aria-expanded="true"')
open(os.path.join(ROOT, 'build/proposal.html'), 'w', encoding='utf-8').write(page)
print('written', len(page))
