#!/usr/bin/env python3
"""Summarise the two SE Ranking "AI Search > Research" CSV exports for a prospect.

Usage: python3 seranking_ai.py <topics.csv> <domains.csv> <prospect-domain> [--off "regex"]

  topics.csv   "Export_research_external_llm_<Firm>_<Month>.csv"
               columns: Topic, topic_size, Volume, Type(Link|Missing), <prospect>, <competitor>..., Brands, AI Engines
  domains.csv  "Export_research_llm_second_part_for_<Firm>.csv"
               columns: Domain, Domain citations, Type, <prospect>, <competitor>..., DT, Org. traffic, Topics

Competitor columns are whatever sits between the prospect column and "Brands"/"DT".
Cells look like "23 (0.18%)": the count is citations (AI linked to that site), not mentions.
"""
import csv, re, sys, collections

topics_f, domains_f, me = sys.argv[1], sys.argv[2], sys.argv[3]
OFF = sys.argv[sys.argv.index("--off") + 1] if "--off" in sys.argv else (
    r"Player|Ministry|Pastoral|Mugshot|Card Benefit|Cardholder|Chargeback|UPC|Unicode|MP3|Resume|"
    r"Travel|Beach|Coastal|Medicaid|Green Card|US Visa|Degree|Sign-On|Metering|Scholarly|Character Profiles")
n = lambda s: int(s.split()[0]) if s and s.strip()[:1].isdigit() else 0

T = list(csv.DictReader(open(topics_f, encoding="utf-8-sig")))
hdr = list(T[0].keys())
i = hdr.index(me)
comps = hdr[i + 1: hdr.index("Brands")]
size_col = hdr[1]
print("competitor columns:", comps)
fake = [c for c in comps if re.search(r"google|chatgpt|perplexity|bing|department|government|commission|tribunal|\bgov\b|legal aid", c, re.I)]
if fake:
    print("NOTE: these tracked 'competitors' are search engines or government bodies, not firms - excluded from firm comparisons:", fake)

print("\n== Total citations across all topics ==")
tot = {c: sum(n(t[c]) for t in T) for c in [me] + comps}
for c, v in sorted(tot.items(), key=lambda x: -x[1]):
    print(f"  {c:30} {v}")

eng = collections.Counter()
for t in T:
    if n(t[me]):
        for e in (t.get("AI Engines") or "").split(","):
            if e.strip():
                eng[e.strip()] += n(t[me])
print("\n== Prospect citations by engine (topic-level tags; overlap, won't sum) ==", dict(eng))

firms = [c for c in comps if c not in fake]
print("\n== Topics where the prospect is cited (on-topic) ==")
print(f"  {'topic':48} {'size':>7} {'me':>4}  " + "  ".join(f"{c[:9]:>9}" for c in firms) + "  verdict")
off_cites = off_n = 0
for t in sorted(T, key=lambda t: -n(t[me])):
    if not n(t[me]):
        continue
    if re.search(OFF, t["Topic"]):
        off_cites += n(t[me]); off_n += 1
        continue
    best = max(firms, key=lambda c: n(t[c]))
    b = n(t[best])
    v = "only firm cited" if b == 0 else ("you lead" if n(t[me]) > b else ("close behind" if n(t[me]) >= b - 2 else f"behind {best}"))
    print(f"  {t['Topic'][:48]:48} {t[size_col]:>7} {n(t[me]):>4}  " + "  ".join(f"{n(t[c]):>9}" for c in firms) + f"  {v}")
print(f"  (excluded as off-topic by --off: {off_n} topics, {off_cites} citations - review the regex per client)")

print("\n== Gap topics: competitors cited, prospect not (sorted by competitor citations) ==")
gaps = [t for t in T if not n(t[me]) and sum(n(t[c]) for c in firms) and not re.search(OFF, t["Topic"])]
for t in sorted(gaps, key=lambda t: -sum(n(t[c]) for c in firms))[:25]:
    who = ", ".join(f"{c} ({n(t[c])})" for c in firms if n(t[c]))
    print(f"  {t['Topic'][:48]:48} {t[size_col]:>7}  {who}  | brands named: {t['Brands']}")

D = list(csv.DictReader(open(domains_f, encoding="utf-8-sig")))
dh = list(D[0].keys())
dcomps = [c for c in dh[dh.index(me) + 1: dh.index("DT")] if c not in fake]
print("\n== Authority: competitors' own domains ==")
for d in D:
    for c in [me] + dcomps:
        key = re.sub(r"[^a-z]", "", c.lower())[:8]
        if key and key in re.sub(r"[^a-z]", "", d["Domain"].lower()):
            print(f"  {c:25} {d['Domain']:35} DT={d['DT']:>3} org.traffic={d['Org. traffic']:>7} own-site citations={d['Domain citations']}")
            break

print("\n== Third-party sites cited next to competitors far more than next to the prospect (reputation targets) ==")
own = re.compile("|".join(re.sub(r"[^a-z]", "", c.lower())[:8] for c in [me] + dcomps if c))
rows = []
for d in D:
    if own.search(re.sub(r"[^a-z]", "", d["Domain"].lower())):
        continue
    c = sum(n(d[x]) for x in dcomps); s = n(d[me])
    rows.append((c - 3 * s, c, s, d["Domain"], d["DT"], {x: n(d[x]) for x in dcomps if n(d[x])}))
for r in sorted(rows, reverse=True)[:25]:
    print(f"  {r[3]:40} with competitors={r[1]:>4} with prospect={r[2]:>3} DT={r[4]:>3} {r[5]}")

print("\n== Sites already cited alongside the prospect (PR / referral / listing targets) ==")
for d in sorted(D, key=lambda d: -n(d[me]))[1:21]:
    print(f"  {d['Domain']:40} {n(d[me]):>3}  DT={d['DT']}")
