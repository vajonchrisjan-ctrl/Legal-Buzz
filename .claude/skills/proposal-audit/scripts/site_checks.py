#!/usr/bin/env python3
"""Measure a prospect's site against the claims a legalbuzz proposal usually makes.

Usage: python3 site_checks.py <work_dir> <domain> [--live]
  work_dir  output of fetch_site.sh (list.txt, pages/, sitemaps/, home.html, robots.txt)
  --live    also run the network checks: footer/redirect probes, public comment count

Prints one block per check. Every number here is something a proposal line can be
compared against; nothing is a verdict on its own.
"""
import collections, glob, html, json, os, re, subprocess, sys, time
from datetime import datetime
from bs4 import BeautifulSoup

W, DOMAIN = sys.argv[1], sys.argv[2]
LIVE = "--live" in sys.argv
BASE = f"https://{DOMAIN}"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"


def fn(u):
    p = re.sub(r"https?://[^/]+/", "", u).rstrip("/").replace("/", "__")
    return os.path.join(W, "pages", p + ".html")


def norm(h):
    h = h.split("#")[0].split("?")[0]
    if h.startswith("/"):
        h = BASE + h
    h = h.replace("http://", "https://").replace("://www.", "://")
    return h if h.endswith("/") else h + "/"


def short(u):
    return u.replace(BASE, "") or "/"


# ---------- parse ----------
listing = [l.split() for l in open(os.path.join(W, "list.txt")) if l.strip()]
team_slugs = [u.rstrip("/").rsplit("/", 1)[1] for k, u in listing if "/team/" in u and u.rstrip("/") != BASE + "/team"]
lawyers = [" ".join(w.capitalize() for w in s.split("-")) for s in team_slugs]

rows = {}
for k, u in listing:
    if k == "O" or not os.path.exists(fn(u)):
        continue
    raw = open(fn(u), errors="ignore").read()
    s = BeautifulSoup(raw, "lxml")
    # Main content: Elementor post/page body, else <main>/<article>, else <body> minus chrome.
    mc = (s.find(attrs={"data-elementor-type": "wp-post"}) or s.find(attrs={"data-elementor-type": "wp-page"})
          or s.find("main") or s.find("article"))
    if mc is None:
        mc = s.body
        for t in mc.find_all(["header", "footer", "nav"]):
            t.decompose()
    txt = mc.get_text(" ", strip=True)
    a_tags = mc.find_all("a", href=True)
    links = [norm(a["href"]) for a in a_tags if DOMAIN in a["href"] or a["href"].startswith("/")]
    ext = [a["href"] for a in a_tags if a["href"].startswith("http") and DOMAIN not in a["href"]]
    allraw = re.findall(r'href="((?:https?://(?:www\.)?' + re.escape(DOMAIN) + r')?/[^"#]*)"', raw)
    ld_people, pub, mod = [], None, None
    for b in s.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(b.string or "")
        except Exception:
            continue
        for x in (d.get("@graph", [d]) if isinstance(d, dict) else d):
            if isinstance(x, dict):
                pub = pub or x.get("datePublished")
                mod = mod or x.get("dateModified")
                if x.get("@type") == "Person":
                    ld_people.append(x.get("name"))
    tables = mc.find_all("table")
    ld_types = re.findall(r'"@type":\s*"([^"]+)"', raw)
    canon = s.find("link", rel="canonical")
    rows[u] = dict(k=k, raw=raw, txt=txt, words=len(txt.split()), links=links, ext=ext, allraw=allraw,
                   pub=pub, mod=mod, tables=len(tables), people=ld_people, types=set(ld_types),
                   canon=canon.get("href") if canon else None, title=(s.title.string if s.title else ""))

A = {u: r for u, r in rows.items() if r["k"] == "A"}
S = {u: r for u, r in rows.items() if r["k"] == "S"}


def head(t):
    print(f"\n=== {t} ===")


head("1. Page counts")
print(f"articles={len(A)} service pages={len(S)} (other sitemap URLs={sum(1 for k,_ in listing if k=='O')})")
print("pages with no main content found:", [short(u) for u, r in rows.items() if r["words"] == 0])

head("2. E-E-A-T: authorship and review")
print("schema Person authors on articles:", collections.Counter(n for r in A.values() for n in (r["people"] or ["<none>"])))
named = {short(u): [l for l in lawyers if re.search(r"\b" + re.escape(l.split()[-1]) + r"\b", r["txt"], re.I)] for u, r in rows.items()}
named = {u: v for u, v in named.items() if v}
print(f"pages whose main content mentions a team member ({len(named)}) - check context, often testimonials:")
for u, v in list(named.items())[:8]:
    print("  ", u, v)
print("'reviewed on/by' wording (check context - often 'decisions are reviewed by a tribunal'):", [short(u) for u, r in rows.items() if re.search(r"reviewed (on|by)", r["txt"], re.I)])
print("first-hand wording ('in our experience' etc):",
      [short(u) for u, r in rows.items() if re.search(r"in our experience|we have seen|we often see|we regularly see", r["txt"], re.I)])

head("3. Information gain")
print("$ amounts (check whether they are fees or just legal thresholds):")
for u, r in rows.items():
    m = re.findall(r".{40}\$\s?\d[\d,]*.{25}", r["txt"])
    if m:
        print("  ", short(u), "|", m[0])
law = lambda r: [e for e in r["ext"] if re.search(r"\.gov\.au|\.gov\.uk|legislation|austlii|bailii|jade\.io|court|tribunal|qcat|vcat|ncat", e)]
lp = [(short(u), r["k"], len(law(r))) for u, r in rows.items() if law(r)]
print(f"pages linking to the law/regulator: {len(lp)} (articles {sum(1 for x in lp if x[1]=='A')}, services {sum(1 for x in lp if x[1]=='S')})", lp)
print("tables in main content:", sum(r["tables"] for r in rows.values()), [short(u) for u, r in rows.items() if r["tables"]])

head("4. Out-of-date references (edit the regex per jurisdiction)")
OLD = r"\bAAT\b|Administrative Appeals Tribunal"   # AU: replaced by the ART on 14 Oct 2024
print([(short(u), len(re.findall(OLD, r["txt"]))) for u, r in rows.items() if re.search(OLD, r["txt"])])

head("5. Thin articles (<400 words of main content)")
for u, r in sorted(A.items(), key=lambda x: x[1]["words"]):
    if r["words"] < 400:
        print(f"  {r['words']:5} {short(u)}  published {r['pub']}")

head("6. Publishing pattern")
ds = sorted(datetime.fromisoformat(r["pub"]) for r in A.values() if r["pub"])
if ds:
    best = max((sum(1 for e in ds if 0 <= (e - d).total_seconds() <= 86400), d) for d in ds)
    print(f"max articles published within 24h: {best[0]} (from {best[1]})")
    print("articles by month:", dict(collections.Counter(d.strftime("%Y-%m") for d in ds)))
print("service pages by month:", dict(collections.Counter((r["pub"] or "?")[:7] for r in S.values())))
grp = collections.defaultdict(list)
for u, r in S.items():
    if r["pub"]:
        grp[r["pub"][:10]].append((r["pub"], short(u)))
for day, v in grp.items():
    if len(v) >= 4:
        v.sort()
        span = (datetime.fromisoformat(v[-1][0]) - datetime.fromisoformat(v[0][0])).total_seconds() / 60
        print(f"  {len(v)} service pages on {day} within {span:.0f} min")

head("7. Internal linking (main content only; menus/footers excluded)")
inb = collections.Counter(l for u, r in rows.items() for l in set(r["links"]) if l != u)
print(f"articles with no inbound link from other article/service bodies: {sum(1 for u in A if inb[u]==0)} of {len(A)}")
print("articles linking to a service page:", [short(u) for u, r in A.items() if any(l in S for l in r["links"])])
print("service pages linking to an article:", [short(u) for u, r in S.items() if any(l in A for l in r["links"])])
print("articles with zero links in AND out:", [short(u) for u, r in A.items() if inb[u] == 0 and not (set(r["links"]) - {u})])
news = os.path.join(W, "pages", "news.html")
if os.path.exists(news):
    n = open(news, errors="ignore").read()
    listed = set(re.findall(r'href="(https?://[^"]*/news/[^"#?]+/)"', n)) - {BASE + "/news/"}
    print(f"news/blog index lists {len(listed)} articles; pagination: {bool(re.search(r'page/2|page-numbers|load more', n, re.I))}")

head("8. Duplicates and canonicals")
print("self-referencing canonicals:", sum(1 for u, r in rows.items() if r["canon"] and r["canon"].rstrip("/") == u.rstrip("/")), "/", len(rows))
def stem(u):
    w = u.rstrip("/").rsplit("/", 1)[1]
    w = re.sub(r"-(lawyers?|law|applications?|solicitors?)$", "", w)
    return w.rstrip("s")
by = collections.defaultdict(list)
for u in S:
    by[stem(u)].append(short(u))
print("possible duplicate service pages (same slug stem - confirm by reading; same slug under different practice areas can be legitimate):", [v for v in by.values() if len(v) > 1])
print("misspelt slugs to eyeball:", [short(u) for u in S if re.search(r"commerical|immigartion|lawer|solictor", u)])

head("9. Schema / entity")
home = open(os.path.join(W, "home.html"), errors="ignore").read()
print("homepage schema types:", sorted(set(re.findall(r'"@type":\s*"([^"]+)"', home))))
print("LegalService/Attorney/LocalBusiness/Organization anywhere:",
      any(t in r["types"] for r in rows.values() for t in ("LegalService", "Attorney", "LocalBusiness", "Organization")))
print("FAQPage anywhere:", any("FAQPage" in r["types"] for r in rows.values()))

head("10. Site-wide problems in the HTML")
tot = len(glob.glob(os.path.join(W, "pages", "*.html")))
for pat, label in [(r"file not found: /[^<]{5,160}", "PHP 'file not found' (leaks server path)"),
                   (r"<b>(?:Warning|Notice|Deprecated|Fatal error)</b>:[^<]{0,160}", "PHP warning")]:
    hits = [f for f in glob.glob(os.path.join(W, "pages", "*.html")) if re.search(pat, open(f, errors="ignore").read())]
    if hits:
        print(f"{label}: on {len(hits)} of {tot} pages ->", re.search(pat, open(hits[0], errors='ignore').read()).group(0)[:160])
cnt = re.findall(r'data-to-value="([^"]+)"|data-(?:end|count|target)="([^"]+)"', home)
if cnt:
    vis = BeautifulSoup(home, "lxml").get_text(" ", strip=True)
    print("animated counters (bots read the starting value, usually 0):", [a or b for a, b in cnt],
          "| visible text sample:", re.findall(r"\b0\+?\s+[A-Z][a-z]+(?: [A-Z][a-z]+)?", vis)[:4])
robots = open(os.path.join(W, "robots.txt"), errors="ignore").read() if os.path.exists(os.path.join(W, "robots.txt")) else ""
print("robots.txt blocks AI bots:", [b for b in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot") if b in robots] or "none named",
      "| 'Disallow: /' present:", bool(re.search(r"^Disallow:\s*/\s*$", robots, re.M)))
for sm in glob.glob(os.path.join(W, "sitemaps", "*.xml")):
    name = os.path.basename(sm)
    if re.search(r"component|custom-category|product|elementor|template|shop", name):
        print(f"junk sitemap {name}: {open(sm).read().count('<loc>')} urls")

if LIVE:
    head("11. Live probes (paced)")
    def curl(*a):
        time.sleep(1.2)
        return subprocess.run(["curl", "-sS", "-A", UA, *a], capture_output=True, text=True).stdout
    hdr = curl("-D", "-", "-o", "/dev/null", f"{BASE}/wp-json/wp/v2/comments?per_page=1")
    m = re.search(r"x-wp-total:\s*(\d+)", hdr, re.I)
    print("public approved comments (often spam):", m.group(1) if m else "endpoint closed")
    if m and int(m.group(1)):
        for c in json.loads(curl(f"{BASE}/wp-json/wp/v2/comments?per_page=5") or "[]"):
            print("   ", c["date"][:10], c["author_name"][:25], "|", re.sub("<[^>]+>", "", c["content"]["rendered"])[:80])
    links = sorted({(BASE + l if l.startswith("/") else l) for r in rows.values() for l in r["allraw"]} |
                   {(BASE + l if l.startswith("/") else l) for l in re.findall(r'href="((?:https?://(?:www\.)?' + re.escape(DOMAIN) + r')?/[^"#]*)"', home)})
    links = [l for l in links if not re.search(r"wp-content|wp-json|xmlrpc|\?", l)]
    print(f"probing {len(links)} distinct internal links for redirects/errors...")
    for l in links:
        out = curl("-o", "/dev/null", "-w", "%{http_code} %{redirect_url}", l)
        if not out.startswith("200"):
            src = [short(u) for u, r in rows.items() if l in [(BASE + x if x.startswith('/') else x) for x in r["allraw"]]][:2]
            print("  ", out, "<-", short(l), "linked from", src or ["home/menu"])
