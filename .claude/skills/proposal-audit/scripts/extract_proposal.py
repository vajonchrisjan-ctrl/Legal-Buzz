#!/usr/bin/env python3
"""Fetch a legalbuzz proposal page and save its text with line numbers for claim-by-claim checking.
Usage: python3 extract_proposal.py <url> <out.txt>
The live page is server-rendered, so plain HTTP is enough. Collapsed dropdowns only show their
titles here; the full copy lives in the Lovable "legalbuzz" project at src/content/<slug>-pitch.md."""
import html, re, sys, urllib.request
url, out = sys.argv[1], sys.argv[2]
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
h = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
h = re.sub(r"<(script|style)\b.*?</\1>", "", h, flags=re.S)
h = re.sub(r"</(p|li|h\d|tr|div)>", "\n", h)
h = re.sub(r"</(td|th)>", " | ", h)
t = html.unescape(re.sub(r"<[^>]+>", " ", h))
lines = [re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()]
open(out, "w").write("\n".join(l for l in lines if l))
print(f"saved {sum(1 for l in lines if l)} lines to {out}")
