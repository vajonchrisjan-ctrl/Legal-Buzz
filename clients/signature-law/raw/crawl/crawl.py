import json, re, time, sys, datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
BASE = "signaturelaw.com.au"
OUT = "/tmp/claude-0/-home-user-Legal-Buzz/f7bb2d48-6446-56fa-85f1-2b4044611aea/scratchpad/crawl"

urls = [l.strip() for l in open(sys.argv[1]) if l.strip()]
results = []
s = requests.Session()
s.headers.update({"User-Agent": UA})

for i, u in enumerate(urls):
    rec = {"url": u, "collected_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        r = s.get(u, timeout=45, allow_redirects=True)
        rec["status"] = r.status_code
        rec["final_url"] = r.url
        rec["redirected"] = (r.url.rstrip('/') != u.rstrip('/'))
        rec["bytes"] = len(r.content)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        t = soup.find("title")
        rec["title"] = t.get_text(strip=True) if t else None
        rec["title_len"] = len(rec["title"]) if rec["title"] else 0

        def meta(name=None, prop=None):
            if name:
                m = soup.find("meta", attrs={"name": re.compile("^"+re.escape(name)+"$", re.I)})
            else:
                m = soup.find("meta", attrs={"property": re.compile("^"+re.escape(prop)+"$", re.I)})
            return m.get("content") if m and m.get("content") else None

        rec["meta_description"] = meta(name="description")
        rec["meta_desc_len"] = len(rec["meta_description"]) if rec["meta_description"] else 0
        rec["meta_robots"] = meta(name="robots")
        rec["viewport"] = meta(name="viewport")
        htag = soup.find("html")
        rec["lang"] = htag.get("lang") if htag else None
        can = soup.find("link", rel=lambda v: v and "canonical" in [x.lower() for x in (v if isinstance(v,list) else [v])])
        rec["canonical"] = can.get("href") if can else None

        for lvl in ["h1","h2","h3"]:
            rec[lvl] = [h.get_text(" ", strip=True) for h in soup.find_all(lvl)]
        rec["h1_count"] = len(rec["h1"])

        og = {}
        tw = {}
        for m in soup.find_all("meta"):
            p = (m.get("property") or "").lower()
            n = (m.get("name") or "").lower()
            if p.startswith("og:"): og[p] = m.get("content")
            if n.startswith("twitter:"): tw[n] = m.get("content")
            if p.startswith("twitter:"): tw[p] = m.get("content")
        rec["og"] = og
        rec["twitter"] = tw
        rec["has_og_image"] = bool(og.get("og:image"))

        imgs = soup.find_all("img")
        rec["img_count"] = len(imgs)
        rec["img_missing_alt"] = sum(1 for im in imgs if im.get("alt") is None)
        rec["img_empty_alt"] = sum(1 for im in imgs if im.get("alt") == "")
        rec["img_srcs"] = [im.get("src") or im.get("data-src") or "" for im in imgs][:40]

        for tag in soup(["script","style","noscript"]):
            tag.decompose()
        text = re.sub(r"\s+"," ", soup.get_text(" ", strip=True))
        rec["word_count"] = len(text.split())
        rec["text_sample"] = text[:1500]

        links = soup.find_all("a")
        internal=[]; external=[]; empty=0
        for a in links:
            href = a.get("href")
            if not href or href.startswith("#") or href.startswith("javascript:"): continue
            full = urljoin(r.url, href)
            host = urlparse(full).netloc.lower().replace("www.","")
            if not a.get_text(strip=True) and not a.find("img"): empty += 1
            if host.endswith(BASE): internal.append(full)
            elif host: external.append(full)
        rec["links_internal"] = len(internal)
        rec["links_internal_unique"] = len(set(internal))
        rec["links_external"] = len(external)
        rec["external_domains"] = sorted(set(urlparse(x).netloc for x in external))
        rec["empty_anchors"] = empty
        rec["forms"] = len(BeautifulSoup(html,"html.parser").find_all("form"))

        soup2 = BeautifulSoup(html, "html.parser")
        ld = []
        for sc in soup2.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}):
            try:
                data = json.loads(sc.string or sc.get_text())
                def types(d):
                    out=[]
                    if isinstance(d, dict):
                        if "@type" in d:
                            tv=d["@type"]
                            out += tv if isinstance(tv,list) else [tv]
                        for v in d.values(): out += types(v)
                    elif isinstance(d, list):
                        for v in d: out += types(v)
                    return out
                ld += types(data)
            except Exception as e:
                ld.append("PARSE_ERROR")
        rec["jsonld_types"] = ld
        rec["jsonld_blocks"] = len(soup2.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}))
        rec["microdata_itemtypes"] = sorted(set(x.get("itemtype") for x in soup2.find_all(attrs={"itemtype":True})))

        low = html.lower()
        rec["tracking"] = {
            "ga4_gtag": bool(re.search(r"gtag\(['\"]config['\"],\s*['\"]G-", html)),
            "ga4_id": re.findall(r"G-[A-Z0-9]{6,12}", html)[:5],
            "ua_legacy": re.findall(r"UA-\d{4,10}-\d", html)[:5],
            "gtm": re.findall(r"GTM-[A-Z0-9]{4,10}", html)[:5],
            "meta_pixel": bool("connect.facebook.net" in low or "fbq(" in low),
            "linkedin": bool("snap.licdn.com" in low),
            "hotjar": bool("hotjar" in low),
            "clarity": bool("clarity.ms" in low),
        }
        rec["tel_links"] = sorted(set(a.get("href") for a in soup2.find_all("a", href=re.compile(r"^tel:", re.I))))
        rec["mailto_links"] = sorted(set(a.get("href") for a in soup2.find_all("a", href=re.compile(r"^mailto:", re.I))))
        rec["phones_in_text"] = sorted(set(re.findall(r"(?:\(0\d\)\s?\d{4}\s?\d{4}|0\d{1}\s?\d{4}\s?\d{4}|1[38]00\s?\d{3}\s?\d{3})", text)))
        rec["abn_acn"] = sorted(set(re.findall(r"(?:ABN|ACN)[:\s]*[\d\s]{9,20}", text, re.I)))
        rec["postcodes"] = sorted(set(re.findall(r"\b(?:NSW|VIC|QLD|WA|SA|TAS|ACT|NT)\s+(\d{4})\b", text)))
    except Exception as e:
        rec["status"] = "FAILED"
        rec["error"] = f"{type(e).__name__}: {e}"
    results.append(rec)
    print(f"[{i+1}/{len(urls)}] {rec.get('status')} {u}", flush=True)
    time.sleep(1.1)

json.dump(results, open(sys.argv[2], "w"), indent=1)
ok = sum(1 for r in results if r.get("status")==200)
print(f"\nDONE: {ok}/{len(results)} returned 200; failed={sum(1 for r in results if r.get('status')=='FAILED')}")
