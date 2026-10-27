import json, re, sys
from pypdf import PdfReader
r=PdfReader('proposal/draft.pdf')
pages=[re.sub(r'\s+',' ',p.extract_text() or '') for p in r.pages]
T={'P1':"Law firms only — and the click",'P2':"One entity, two registered names",'P3':"Every service has a page. Almost none",
 'P4':"An assistant can only recommend",'P5':"32 out of 100 — and the lowest",'P6':"A well-built site that does not describe",
 'P7':"One decision first, then nineteen",'P8':"Fix, build, then earn trust and measure",'P9':"Good bones, no voice",
 'P10':"Three scopes. No fee in this",'P11':"Every number above, and where"}
pm={}
for k,t in T.items():
    hit=[i+1 for i,n in enumerate(pages) if t in n and i>1]   # skip cover + contents page itself
    pm[k]=hit[0] if hit else None
print(pm)
json.dump(pm,open('proposal/pagemap.json','w'))
sys.exit(1 if None in pm.values() else 0)
