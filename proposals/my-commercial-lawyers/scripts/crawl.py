import sys,re,json,html,time,urllib.request
urls=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out=[]
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) Chrome/130'})
    with urllib.request.urlopen(r,timeout=40) as f: return f.status,f.read().decode('utf-8','ignore')
for u in urls:
    try: st,s=get(u)
    except Exception as e: out.append({'url':u,'err':str(e)}); time.sleep(4); continue
    F=lambda p:re.findall(p,s,re.I|re.S)
    clean=lambda x:html.unescape(re.sub('<[^>]+>','',x)).strip()
    lds=[]
    for b in F(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>'):
        try:
            d=json.loads(b); g=d.get('@graph',[d]) if isinstance(d,dict) else d
            for x in g:
                t=x.get('@type'); lds+= t if isinstance(t,list) else [t]
        except: lds.append('ERR')
    body=re.sub(r'<header.*?</header>|<footer.*?</footer>|<script.*?</script>|<style.*?</style>|<nav.*?</nav>','',s,flags=re.S|re.I)
    words=len(html.unescape(re.sub('<[^>]+>',' ',body)).split())
    m=lambda n:(F(r'<meta[^>]+(?:name|property)=["\']%s["\'][^>]*content=["\']([^"\']*)'%n) or [None])[0]
    out.append({'url':u,'status':st,'title':clean((F(r'<title[^>]*>(.*?)</title>') or [''])[0]),
     'desc':m('description'),'robots':m('robots'),'h1':[clean(x) for x in F(r'<h1[^>]*>(.*?)</h1>')],
     'h2n':len(F(r'<h2[\s>]')),'words':words,'schema':lds,'og':len(F(r'property=["\']og:')),
     'author':m('author'),'pub':m('article:published_time'),'mod':m('article:modified_time'),
     'sra':len(F(r'SRA|Solicitors Regulation')),'tel':len(F(r'href=["\']tel:')),
     'imgs_noalt':len(F(r'<img(?![^>]*alt=["\'][^"\']+)[^>]*>'))})
    print(u,st,words,flush=True)
    time.sleep(4)
json.dump(out,open(sys.argv[2],'w'),indent=1)
