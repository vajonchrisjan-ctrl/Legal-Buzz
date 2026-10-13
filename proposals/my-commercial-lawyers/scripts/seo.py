# Blocks built from the SE Ranking data pack (Google UK database, pulled 13 October 2026).
import json, os
from comp import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'ser/organic.json'), encoding='utf-8'))
KW, PAGES = D['kw'], D['pages']
PG = {p['url']: p for p in PAGES}
FIRM = 'My Commercial Lawyers'

REDIRECTED = {'/what-are-the-defences-to-criminal-liability-within-uk-law/', '/what-are-the-penalties-for-health-and-safety-in-the-uk/', '/new-uk-construction-retentions-reporting-rules-2025/', '/contact-us/'}
SERVICE = {'/construction-contract-disputes/', '/construction-law-firm-london/', '/debt-recovery/', '/unpaid-construction-invoices/', '/breach-of-contract-lawyer-near-me/', '/breach-of-contract/', '/construction-disputes/'}
OTHER = {'/case-studies/', '/contact-my-commercial-lawyers/', '/privacy-policy/', '/contact-us/'}

def kv(url):
    p = PG.get(url)
    return f"{p['kw']} / {p['tr']}" if p else '0 / 0'

def page_split():
    home = PG['/']['kw']
    svc = sum(PG[u]['kw'] for u in SERVICE if u in PG)
    red = sum(PG[u]['kw'] for u in REDIRECTED - {'/contact-us/'} if u in PG)
    oth = sum(PG[u]['kw'] for u in OTHER if u in PG)
    guides = sum(p['kw'] for p in PAGES) - home - svc - red - oth
    return home, guides, red, oth, svc

def keyword_fig():
    home, guides, red, oth, svc = page_split()
    parts = [('bg-muted-foreground/40', home, 'Homepage'), ('bg-muted-foreground/60', guides, 'Guides still live'), ('bg-muted-foreground/80', red, 'Posts now redirected'), ('bg-secondary/60', oth, 'Contact, case studies, privacy'), ('bg-destructive', svc, 'Service and location pages')]
    bar = ''.join(f'<div class="{c} flex items-center justify-center text-xs font-bold text-primary-foreground" style="flex-grow: {v}; flex-basis: 0">{v if v >= 12 else ""}</div>' for c, v, _ in parts)
    leg = ''.join(f'<li class="flex items-center gap-2"><span class="h-3 w-3 rounded-sm {c}"></span><span class="{"font-bold" if c == "bg-destructive" else "text-foreground/75"}">{n} <span class="tabular-nums">({v})</span></span></li>' for c, v, n in parts)
    total = home + guides + red + oth + svc
    return fig('Where your keywords actually sit', f'{total} page-keyword rankings across 24 URLs. Only {svc} sit on the service and location pages built to win instructions, and they bring in no measurable visits.',
               f'<div class="flex h-14 overflow-hidden rounded-lg">{bar}</div><ul class="mt-5 grid gap-2 text-sm sm:grid-cols-3">{leg}</ul>')

def serp_fig():
    org = ['Osbornes Law: construction disputes page', 'Legal 500: London construction rankings', 'B P Collins: construction disputes page', 'Forsters: construction disputes page', 'Russell-Cooke: construction disputes page', 'JHA (uk.jha.com): construction page']
    lis = ''.join(f'<li class="flex items-center gap-3 rounded-lg bg-background px-4 py-2.5 text-sm ring-1 ring-border"><span class="w-5 text-xs font-bold text-muted-foreground">{i}</span>{n}</li>' for i, n in enumerate(org, 1))
    maps = ''.join(f'<li class="flex justify-between gap-2"><span>{"<strong>" + n + "</strong>" if "Commercial" in n else n}</span><span class="text-accent">{t}</span></li>' for n, t in [('My Commercial Lawyers', '#1'), ('Nath Solicitors', '#2'), ('Fenwick Elliott LLP', '#3')])
    return fig('The London test', 'What a contractor sees for "construction dispute solicitor london". SE Ranking stored results page, Google UK, 13 October 2026.',
        f'''<div class="mx-auto max-w-2xl overflow-hidden rounded-xl bg-surface ring-1 ring-border"><div class="flex items-center gap-3 border-b border-border bg-background px-4 py-3">{SEARCH}<span class="text-sm">construction dispute solicitor london</span></div>
<div class="space-y-4 p-4"><div class="rounded-lg bg-background p-4 ring-1 ring-border"><p class="flex items-center gap-2 text-xs font-bold tracking-wide text-secondary uppercase">{SPARK()} AI Overview</p><p class="mt-2 text-sm text-foreground/80">Cites Russell-Cooke, Osbornes Law, Forsters, B P Collins, JHA and Trowers &amp; Hamlins. My Commercial Lawyers is not cited.</p></div>
<div class="rounded-lg bg-background p-4 ring-1 ring-border"><p class="flex items-center gap-2 text-xs font-bold tracking-wide text-secondary uppercase">{PIN()} Maps pack</p><ul class="mt-2 space-y-1.5 text-sm">{maps}</ul></div>
<ol class="space-y-2">{lis}</ol>
<div class="flex items-center gap-3 rounded-lg border-2 border-dashed border-destructive px-4 py-3 text-sm font-bold text-destructive">{XICON}My Commercial Lawyers (website): not in the top 100</div></div></div>''')

def serp_table():
    return table(['Search', 'Searches / month', 'Google Maps pack', 'Page one organic', FIRM], [
        ['construction dispute solicitor london', '0 tracked (difficulty 8)', '<strong>My Commercial Lawyers #1</strong>, Nath Solicitors, Fenwick Elliott', 'Osbornes Law, Legal 500, B P Collins, Forsters, Russell-Cooke, JHA, Dutton Gregory, Trowers &amp; Hamlins', 'Maps #1; website not in top 100'],
        ['commercial litigation solicitor london', '40 (difficulty 11)', 'Forest &amp; Co, Summit Law, <strong>My Commercial Lawyers #3</strong>', 'Summit Law, Legal 500, Saunders, Russell-Cooke, Oliver Fisher, Mishcon de Reya, Weightmans, Chambers', 'Maps #3; website not in the organic list'],
        ['commercial lawyer london', '70 (difficulty 13)', 'Branch Austin McCormick, Summit Law, Gannons', 'Not stored in the pack', 'Organic #9; not in the Maps pack'],
        ['construction solicitor croydon', 'Not in SE Ranking\'s UK database', 'n/a', 'n/a', 'To track directly from month one'],
    ])

def quick_wins():
    rows = [['commercial lawyer london', '70', '13', '#9', 'Homepage'], ['commercial lawyers', '320', '17', '#1 and #11', 'Homepage'], ['commercial litigation barristers', '50', '15', '#10', 'Homepage'],
            ['commercial dispute resolution barristers', '30', '5', '#11', 'Homepage'], ['construction solicitors near me', '20', '4', '#11', 'Homepage'], ['construction lawyers near me', '40', '11', '#12', 'Homepage'],
            ['commercial property dispute', '110', '4', '#12', 'Homepage'], ['commercial litigation london', '20', '11', '#11', 'Homepage']]
    return table(['Keyword', 'Searches / month', 'Difficulty', 'Today', 'Page ranking now'], rows)

def kw_service():
    return table(['Service', 'Keywords worth owning (searches a month, difficulty, where you rank today)', 'Page that wins it'], [
        ['Construction disputes', 'construction solicitors 320 (5, you rank #54); construction dispute solicitors 260 (13, #41); construction dispute lawyer 210 (15, #46); lawyers construction disputes 210 (17, #47); construction law lawyers 260 (15, #59)', 'London construction disputes hub'],
        ['Building disputes', 'building dispute solicitors 320 (11, #52); solicitors for building disputes 320 (7, #55); builder disputes solicitors 320 (12, #51); solicitors specialising in building disputes near me 140 (10, #39)', 'A building disputes page under the construction pillar'],
        ['Adjudication', 'construction adjudication solicitor 40 (16, not ranking); pay less notice 480 (5, not ranking)', 'One adjudication pillar (merging the two pages)'],
        ['Payment and retention', 'retention construction 260 (6, #74); construction retention 260 (7, #77); unpaid invoice solicitor 10 (6, #47)', 'Unpaid invoices and retention pillar'],
        ['Commercial disputes', 'commercial solicitors 990 (13, #57); contract dispute solicitors 390 (11, #52); commercial dispute solicitors 260 (13, #70); breach of contract solicitor 140 (4, not ranking); business dispute lawyer 140 (21, not ranking)', 'Commercial disputes pillar'],
        ['Debt recovery', 'letter before action 2,900 (37, not ranking); business debt recovery 260 (16, not ranking); commercial debt recovery solicitor 110 (4, #93)', 'Debt recovery pillar with the fee answer'],
        ['International', 'uk dispute lawyer for overseas company and international arbitration lawyer uk: not in SE Ranking\'s UK database', 'International hub, tracked directly'],
    ])

def kw_london():
    return table(['Keyword', 'Searches / month', 'Difficulty', 'Today', 'Page we build'], [
        ['construction dispute solicitor london', '0 tracked', '8', 'Maps #1; website not in top 100', 'London hub'],
        ['construction lawyer london', '50', '15', '#55', 'London hub'],
        ['construction lawyers london', '50', '20', '#42', 'London hub'],
        ['construction solicitor london', '30', '13', '#61', 'London hub'],
        ['commercial litigation solicitor london', '40', '11', 'Maps #3', 'Commercial disputes pillar'],
        ['jct contract dispute solicitor london', 'Not in UK database', 'n/a', 'n/a', 'JCT in London'],
        ['construction lawyer city of london', 'Not in UK database', 'n/a', 'n/a', 'City of London page'],
    ])

def kw_croydon():
    return table(['Keyword', 'Searches / month', 'Difficulty', 'Page we build'], [
        ['construction solicitor croydon', 'Not in UK database', 'n/a', 'Croydon page'],
        ['commercial lawyer croydon', 'Not in UK database', 'n/a', 'Croydon page'],
        ['commercial lawyer croydon cost', 'Not in UK database', 'n/a', 'Croydon cost guide'],
    ])

def competitors_tbl():
    rows = [[f'<strong>{FIRM}</strong>', '365', '94', '195', '50', '10', 'You']]
    for d, kw, tr, rd, dt, note in [
        ('mymsolicitors.co.uk', 397, 670, 122, 26, 'Name lookalike'), ('combar.com', 508, 374, 668, 66, 'Commercial Bar Association'), ('bsdgb.co.uk', 525, 306, 222, 26, 'Criminal defence'),
        ('eve.legal', 231, 238, '1.1K', 73, 'Legal AI software'), ('ksclegal.co.uk', 426, 96, 42, 4, 'Unverified'), ('mylegalsolicitors.co.uk', 108, 46, 67, 21, 'Name lookalike'),
        ('cbl.law', 165, 40, 53, 34, 'Unverified'), ('mylondonsolicitors.com', 60, 33, 58, 8, 'Name lookalike'), ('mbconsultancy.com.au', 35, 12, 50, 32, 'Australian consultancy'), ('mylawlegal.co.uk', 78, 8, 7, 4, 'Name lookalike')]:
        rows.append([d, str(kw), 'n/a', str(tr), str(rd), str(dt), note])
    return table(['Domain', 'Keywords', 'Top 10', 'Est. visits / mo', 'Referring domains', 'Domain trust', 'Who they are'], rows)

def traffic_fig():
    rows = [('mymsolicitors.co.uk', 670, False), ('combar.com', 374, False), ('bsdgb.co.uk', 306, False), ('eve.legal', 238, False), (FIRM, 195, True), ('ksclegal.co.uk', 96, False), ('mylegalsolicitors.co.uk', 46, False), ('cbl.law', 40, False)]
    return fig('Estimated Google visits a month', 'SE Ranking, Google UK, October 2026. Your 195 visits are worth about $1.2K a month in ads; 190 of them land on the homepage.', hbars(rows, maxv=700, fmt=lambda v: f'{v:,}'))

def page_one_tbl():
    return table(['Firm', 'Where it appears for your London searches', 'What it has that you do not'], [
        ['Osbornes Law', 'First organic result and cited in the AI Overview, "construction dispute solicitor london"', 'A dedicated construction disputes page; mobile score 100, main content in 1.1s'],
        ['B P Collins', 'Third organic result and cited in the AI Overview', 'A dedicated construction disputes page (mobile score 39, so speed is not what wins it)'],
        ['Forsters', 'Fourth organic result and cited in the AI Overview', 'A construction disputes page inside a dispute resolution hub'],
        ['Russell-Cooke', 'Fifth organic result and cited in the AI Overview; also on page one for commercial litigation', 'Service pages for both construction and commercial litigation'],
        ['Legal 500', 'Second organic result for both London searches', 'The directory itself: being listed puts you on page one through it'],
        ['Summit Law', 'First organic result and Maps #2 for commercial litigation; Maps #2 for commercial lawyer london', 'A commercial litigation page plus a strong Maps profile'],
        ['Nath Solicitors, Fenwick Elliott', 'Maps #2 and #3 behind you for construction dispute solicitor london', 'Map presence only; you already beat them there'],
    ])

def maps_tbl():
    return table(['Search', 'Maps #1', 'Maps #2', 'Maps #3', FIRM], [
        ['construction dispute solicitor london', '<strong>My Commercial Lawyers</strong>', 'Nath Solicitors', 'Fenwick Elliott LLP', '#1'],
        ['commercial litigation solicitor london', 'Forest &amp; Co Solicitors', 'Summit Law LLP', '<strong>My Commercial Lawyers</strong>', '#3'],
        ['commercial lawyer london', 'Branch Austin McCormick LLP', 'Summit Law LLP', 'Gannons Solicitors', 'Not in the pack'],
    ])

LIMIT = 10
OTHER_FIRMS = {'comer law office','giannakopoulos solicitors','lowless commercial solicitors','hlw commercial lawyers','macbeth currie solicitors','mcleods barristers and solicitors','mcleod\'s barristers and solicitors','mycra lawyers','cm lawyers','cmc lawyers','amc lawyers','mhd solicitors','macy law firm','mays law office','mcadvo','gve commercial solutions','con lavery','andrew onslow kc','paul pavlou barrister','douglas mcevoy','mark hackett associates','mark lorrell solicitor','chinatown market call my lawyer'}
ADDR = {'wc2a 3ta','7 savoy court london wc2r 0ex'}

def rankings_tbl():
    rows = []
    def label(u):
        return 'Homepage' if u == '/' else u.strip('/').replace('-', ' ')[:48] + (' (now redirected)' if u in REDIRECTED else '')
    order = ['/'] + [p['url'] for p in sorted(PAGES, key=lambda p: -p['kw']) if p['url'] != '/']
    for u in order:
        ks = sorted([k for k in KW if k['url'] == u and k['pos'] <= LIMIT], key=lambda k: (-k['vol'], k['pos']))
        seen = set()
        for k in ks:
            if k['pos'] > LIMIT: continue
            if k['k'] in seen: continue
            seen.add(k['k'])
            typ = 'Another firm\'s name' if k['k'] in OTHER_FIRMS else 'Address or postcode' if k['k'] in ADDR else 'Brand / name lookalike' if any(x in k['k'] for x in ['my ', 'mcl', 'mc ', 'mcleod', 'm y ']) or k['k'] in ('my lawyer', 'my lawyers', 'your lawyer', 'my law firm') else ('Off-topic' if u in REDIRECTED and u != '/new-uk-construction-retentions-reporting-rules-2025/' else 'Commercial' if u == '/' or u in SERVICE else 'Informational')
            rows.append([label(u), k['k'], str(k['vol']), str(k['pos']), typ])
    return rows

def rankings_acc():
    rows = rankings_tbl()
    return acc(f'All {len(rows)} keywords in the top 10', 'Grouped by the page that ranks; the full 413-row list is in the SE Ranking data pack', table(['Page', 'Keyword', 'Searches / mo', 'Position', 'Type'], rows))
