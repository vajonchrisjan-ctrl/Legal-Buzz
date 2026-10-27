import sys, os
B='/tmp/claude-0/-home-user-Legal-Buzz/f7bb2d48-6446-56fa-85f1-2b4044611aea/scratchpad'
order=['p01-cover','p02-questions','p03-sec1','p05-sec3','p07-sec5','p08-sec5b',
       'p09-sec6','p11-sec7','p12-sec7b','p13-sec8','p14-sec9-10','p16-sec11']
head=open(f'{B}/proposal/head.html').read()
head=head.replace('__FONTS__', open(f'{B}/fonts/embedded.css').read())
body=''.join(open(f'{B}/proposal/{n}.html').read() for n in order)
html=head+body
import re as _re
# header row of every table -> <thead> so it repeats when a table splits across pages
html=_re.sub(r'(<table>\s*)(<tr>(?:\s*<th[^>]*>.*?</th>)+\s*</tr>)', lambda m: m.group(1)+'<thead>'+m.group(2)+'</thead>', html, flags=_re.S)
total=html.count('<div class="page"')
html=html.replace('__TOTAL__',str(total))
# page-number tokens, supplied by caller after a render pass
import json
pg=json.load(open(f'{B}/proposal/pagemap.json')) if os.path.exists(f'{B}/proposal/pagemap.json') else {}
for k,v in pg.items():
    html=html.replace('{{%s}}'%k,str(v))

# section opener: navy block -> live-page style (badge + label, headline, intro)
def _sec(m):
    num=int(m.group(1)); label=m.group(2); hid=m.group(3); head=m.group(4); intro=m.group(5)
    return (f'<div class="sectop"><div class="sechead"><span class="badge">{num}</span><span>{label}</span></div>'
            f'<h2 class="headline" id="{hid}">{head}</h2><p class="secintro">{intro}</p></div>')
html=_re.sub(r'<div class="sec"><div class="num">(\d+)</div><div class="kicker">(.*?)</div>\s*<h2 id="(S\d+)">(.*?)</h2>\s*<p>(.*?)</p></div>',_sec,html,flags=_re.S)
# bordered 4px wrapper around every table
html=html.replace('<table>','<div class="tw"><table>').replace('</table>','</table></div>')
open(f'{B}/proposal/proposal.html','w').write(html)
print('pages declared:',total,'| html bytes:',len(html),'| tokens left:',html.count('{{P'))
