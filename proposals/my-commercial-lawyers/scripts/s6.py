# Section 6 built from SE Ranking AI Search (UK, October 2026) exports and screenshots.
import csv, os
from comp import *
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIRM = 'My Commercial Lawyers'
topics = list(csv.DictReader(open(os.path.join(ROOT, 'ser/topics.csv'), encoding='utf-8')))
cites = list(csv.DictReader(open(os.path.join(ROOT, 'ser/citations.csv'), encoding='utf-8')))
ENG = {'aio': 'Google AI Overviews', 'perplexity': 'Perplexity', 'chatgpt': 'ChatGPT'}
OFF = {'Safety and Adverse Event Reporting', 'Construction Safety Management', 'Invoicing and Billing Software', 'Spell Compendium and Search', 'Criminal Defense Representation', 'Construction Management Services'}

def build(DATE):
    topic_rows = []
    for r in topics:
        n, pct = r['Presence'].split(' ', 1)
        name = r['Topic'] + (' <span class="text-xs text-destructive">(not a service you sell)</span>' if r['Topic'] in OFF else '')
        topic_rows.append([name, f"{int(r['research.table.headers.topic_size']):,}", f'{n} {pct}', ', '.join(ENG.get(e.strip(), e.strip()) for e in r['AI Engines'].split(','))])
    off_n = sum(int(r['Presence'].split()[0]) for r in topics if r['Topic'] in OFF)
    keep = ['www.legal500.com', 'chambers.com', 'en.wikipedia.org', 'www.chartlands.org', 'lawtutor.co.uk', 'www.waldrons.co.uk', 'www.michelmores.com', 'bateswells.co.uk', 'www.pinsentmasons.com', 'www.fenwickelliott.com', 'www.sra.org.uk']
    byd = {r['Domain']: r for r in cites}
    src_rows = [[d.replace('www.', ''), byd[d]['Presence'].split()[0], byd[d]['DT'], byd[d]['Topics'].split(', ')[0] + (' and more' if ', ' in byd[d]['Topics'] else '')] for d in keep if d in byd]
    me = byd['www.mycommerciallawyers.com']
    src_rows.insert(0, [f'<strong>mycommerciallawyers.com</strong>', me['Presence'].split()[0], me['DT'], 'Your own pages (17 topics)'])

    topic_tbl = table(['Topic', 'mycommerciallawyers.com', 'ksclegal.co.uk', 'combar.com', 'mbconsultancy.com.au', 'cbl.law', 'bsdgb.co.uk'], [
        ['Litigation and Dispute Resolution', '<strong>0.07%</strong>', '0%', '0.02%', '0%', '0%', '0%'],
        ['Corporate Lawyer Listings', '<strong>0.02%</strong>', '0.02%', '0.06%', '0%', '0.01%', '0%'],
        ['Civil Litigation and Lawsuit Representation', '<strong>0.09%</strong>', '0.05%', '0%', '0%', '0%', '0%'],
        ['Commercial Litigation and Dispute Resolution', '<strong>0.21%</strong>', '0.32%', '0.53%', '0%', '0%', '0%'],
        ['Legal Dictionary and Reference Content', '<strong>0.01%</strong>', '0%', '0%', '0%', '0%', '0%'],
    ])
    sov = fig('AI share of voice: Commercial Litigation and Dispute Resolution', 'Share of 948 tracked UK prompts whose AI answer cites each site. Google AI Overviews, AI Mode, ChatGPT, Perplexity and Gemini. SE Ranking AI Search, October 2026.',
              hbars([('combar.com', 0.53, False), ('ksclegal.co.uk', 0.32, False), (FIRM, 0.21, True), ('mbconsultancy.com.au', 0, False), ('cbl.law', 0, False), ('bsdgb.co.uk', 0, False)], maxv=0.6, fmt=lambda v: f'{v:g}%'))
    engines = fig('AI presence by engine, April to October 2026', 'Share of tracked prompts citing your site, read from the SE Ranking AI Search trend (approximate).',
        '<div class="grid gap-3 sm:grid-cols-3">'
        + '<div class="rounded-xl bg-surface p-5 ring-1 ring-border"><p class="font-display text-2xl font-bold text-primary">0.3 to 0.5%</p><p class="mt-1 text-sm text-foreground/75"><strong>Perplexity.</strong> Your steadiest engine, flat across six months.</p></div>'
        + '<div class="rounded-xl bg-surface p-5 ring-1 ring-border"><p class="font-display text-2xl font-bold text-destructive">1.2% to 0%</p><p class="mt-1 text-sm text-foreground/75"><strong>Google AI Mode.</strong> Climbed through July to a peak in early August, then fell to zero from September and has not come back.</p></div>'
        + '<div class="rounded-xl bg-surface p-5 ring-1 ring-border"><p class="font-display text-2xl font-bold text-destructive">Near 0%</p><p class="mt-1 text-sm text-foreground/75"><strong>AI Overviews, ChatGPT, Gemini.</strong> Occasional citations only. ChatGPT cited you in spring and has barely since.</p></div>'
        + '</div>')
    ai_fix = table(['What AI needs', 'Today on your site', 'The fix', 'When'], [
        ['To say your name', 'Cited in 27 answers, named in none (SE Ranking: mentions, no data)', 'One consistent brand line on every page and in schema: "My Commercial Lawyers, barrister-led construction and commercial dispute practice, London"', 'Month 1'],
        ['To know where you are', 'No address on the contact page or in schema; registered address only in the footer', 'One verified address (or service-area profile), identical on site, schema and Google', 'Month 1'],
        ['To know who stands behind the advice', 'One unverified author account on all 40 guides; no lawyer profiles', 'A profile and Person schema for each barrister and solicitor; every guide signed or reviewed', 'Month 1 to 2'],
        ['To know you are regulated', 'BSB reference in the footer text only', 'BSB reference in LegalService schema, linked to the register, on every page', 'Month 1'],
        ['To find your services', 'llms.txt lists only blog posts; 0 of 24 service and location pages', 'Hand-written llms.txt: services and locations first, then guides', 'Week 2'],
        ['To cite you for the right things', f'{off_n} of your 27 citations are for topics you do not sell (safety reporting, billing software, spelling)', 'Retire or refocus the off-topic posts; link every guide to a service pillar', 'Month 1 to 2'],
        ['To be able to read the site', 'GPTBot, OAI-SearchBot, ClaudeBot and PerplexityBot all allowed (verified)', 'Keep it that way through the rebuild', 'Done'],
        ['Others to agree with you', 'Legal 500 and Chambers are cited in your topics; you are not listed where AI looks; domain trust 10', 'Legal 500, Chambers, BSB register, Law Society and construction press listings, all with the same name, address and phone', 'Month 2 onwards'],
    ])
    return section(6, 'What AI says about you', 'What AI says about you',
        p('How we measured: SE Ranking AI Search tracks which brands and links appear in Google AI Overviews, Google AI Mode, ChatGPT, Perplexity and Gemini answers in the UK, from April to October 2026. We compared you with the five competitors SE Ranking suggests for your topics. Alongside it, we checked everything on your own site that decides whether AI can cite you at all.')
        + stats([('0.01%', 'overall AI presence in the UK, down 0.001 points this month'), ('0', 'AI answers that name My Commercial Lawyers (SE Ranking finds no brand mentions)'), ('27', 'AI answers that cite a page on your site'), ('17', 'topics those citations fall in, six of them topics you do not sell')])
        + sov
        + p(f'<em class="text-sm text-muted-foreground not-italic">SE Ranking\'s suggested competitor set includes an Australian consultancy (mbconsultancy.com.au) and a criminal defence site (bsdgb.co.uk). In month one we replace them with the London construction and commercial dispute firms you actually compete with, so the share of voice we report is against real rivals.</em>')
        + acc('Topic presence: you against the five suggested competitors', 'Share of prompts in each topic whose AI answer cites the site', topic_tbl)
        + engines
        + h3('Where you are already winning')
        + cards([
            ('AI already uses your pages as sources.', 'Twenty-seven AI answers cite mycommerciallawyers.com, across Google AI Overviews, Perplexity and ChatGPT. Your writing is good enough to be quoted. It just is not yet good enough to be recommended.'),
            ('You lead on litigation topics.', 'In "Litigation and Dispute Resolution" (0.07%) and "Civil Litigation and Lawsuit Representation" (0.09%) you are cited more than every suggested competitor. That is with no lawyer profiles, no address and domain trust of 10.'),
            ('AI can read the site.', 'Every major AI crawler we tested (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot) gets the page. FAQ schema on 26 pages and question-shaped guides give AI answers in the shape it wants.'),
        ])
        + h3('What AI does not know')
        + cards([
            ('Your name.', 'Cited 27 times, named zero times. AI uses your pages to explain the law, then recommends someone else. A source is not a recommendation; the fix list below is what turns one into the other.', 'border-destructive'),
            ('Where you are and who your lawyers are.', 'No office address on the site or in the schema, no lawyer profiles, and every guide signed by an author who is not on the team. AI cannot place you in London or attach your advice to a barrister.', 'border-destructive'),
            ('What you actually sell.', f'{off_n} of your 27 citations sit in topics such as "Safety and Adverse Event Reporting", "Invoicing and Billing Software" and "Spell Compendium and Search". And Google AI Mode, your best engine in the summer, dropped you to zero in September.', 'border-destructive'),
        ])
        + h3('The sources AI trusts in your topics')
        + p('The domains cited most often in the same AI answers. Legal 500 and Chambers are cited for "Corporate Lawyer Listings" and "Law Firm Legal Services", the topics where AI picks a firm. That is where your name needs to be.')
        + acc('Who else AI cites, and how much it trusts them', 'Answers citing each domain in your topics, with SE Ranking domain trust (DT)', table(['Domain', 'AI answers citing it', 'Domain trust', 'Main topic'], src_rows))
        + h3('Your AI-citation fix list')
        + p('Everything AI needs before it will name a firm, what your site gives it today, and when we fix it. Site entries were checked on the live site on ' + DATE + '; AI entries are from SE Ranking AI Search, October 2026.')
        + ai_fix
        + h3('The AI answers you appear in today')
        + p('Every topic in SE Ranking\'s UK AI index where an answer cites one of your pages. Not one of them names you.')
        + acc('All 17 topics, one by one', f'27 citations, 0 mentions; {off_n} citations in topics you do not sell', table(['Topic', 'Prompts tracked', 'Answers citing you', 'Engines'], topic_rows))
        + plain('Businesses now ask ChatGPT and Google AI "who is a good construction dispute solicitor in London" and "how much does adjudication cost". AI already reads your pages to answer questions about litigation, then names a firm whose address, lawyers and listings it can check. Close that gap and the 27 citations become recommendations.'), alt=True)
