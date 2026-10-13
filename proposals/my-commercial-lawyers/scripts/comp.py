# Component helpers reproducing the legalbuzz proposal template markup exactly.
import html as _h
E=lambda s:s  # content is authored as HTML-safe strings already
CHEV='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-down mt-1 h-5 w-5 shrink-0 text-muted-foreground transition-transform rotate-180" aria-hidden="true"><path d="m6 9 6 6 6-6"></path></svg>'
ARROW_R_SM='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right absolute top-1/2 -right-4 z-10 hidden h-6 w-6 -translate-y-1/2 rounded-full bg-accent p-1 text-accent-foreground md:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>'
ARROW_R_LG='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right absolute top-1/2 -right-4 z-10 hidden h-7 w-7 -translate-y-1/2 rounded-full bg-accent p-1.5 text-accent-foreground lg:block" aria-hidden="true"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>'
ARROW_D='<div class="flex justify-center py-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-down h-5 w-5 text-accent" aria-hidden="true"><path d="M12 5v14"></path><path d="m19 12-7 7-7-7"></path></svg></div>'
CHECK=lambda c='text-success':f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check mt-0.5 h-4 w-4 shrink-0 {c}" aria-hidden="true"><path d="M20 6 9 17l-5-5"></path></svg>'
SEARCH='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search h-4 w-4 text-muted-foreground" aria-hidden="true"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>'
SPARK=lambda c='h-3.5 w-3.5':f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles {c}" aria-hidden="true"><path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"></path><path d="M20 2v4"></path><path d="M22 4h-4"></path><circle cx="4" cy="20" r="2"></circle></svg>'
PIN=lambda c='h-3.5 w-3.5':f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map-pin {c}" aria-hidden="true"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"></path><circle cx="12" cy="10" r="3"></circle></svg>'
XICON='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x h-4 w-4" aria-hidden="true"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>'
PHONE='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-smartphone h-5 w-5 shrink-0 text-accent" aria-hidden="true"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"></rect><path d="M12 18h.01"></path></svg>'
SEARCHBIG='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search h-6 w-6 text-secondary" aria-hidden="true"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>'

def section(n,label,title,body,alt=False):
    bg=' bg-surface/50' if alt else ''
    return f'''<div><section id="s{n}" data-chip="" class="scroll-mt-36 py-20 lg:py-28{bg}"><div class="band-x mx-auto max-w-6xl">
<p class="mb-5 inline-flex items-center gap-3 text-xs font-bold tracking-[0.2em] text-secondary uppercase"><span class="flex h-7 w-7 items-center justify-center rounded-full bg-primary text-[11px] text-accent">{n}</span>{label.upper()}</p>
<h2 class="font-display font-bold leading-[1.02] text-balance text-4xl lg:text-6xl mb-6">{title}</h2>
{body}</div></section></div>'''
def p(t): return f'<p class="my-4 max-w-3xl leading-relaxed text-foreground/85">{t}</p>'
def b(t): return f'<strong class="font-semibold text-foreground">{t}</strong>'
def small(t): return p(f'<em class="text-sm text-muted-foreground not-italic">{t}</em>')
def h3(t): return f'<h3 class="mt-12 mb-4 font-display text-2xl font-bold lg:text-3xl">{t}</h3>'
def h4(t): return f'<h4 class="mt-8 mb-3 font-display text-lg font-bold">{t}</h4>'
def plain(t): return f'<div><div class="my-8 max-w-3xl rounded-xl border-l-4 border-accent bg-accent/15 px-6 py-5 [&amp;_p]:my-0">{p(b("In plain English:")+" "+t)}</div></div>'
def quote(t): return f'<blockquote>{p(t)}</blockquote>'
def pending(t): return f'<span class="rounded bg-accent px-1.5 py-0.5 text-xs font-bold text-accent-foreground">{t}</span>'
def stats(items,cols=4,dark=False):
    g={3:'sm:grid-cols-3',4:'sm:grid-cols-2 lg:grid-cols-4',2:'sm:grid-cols-2'}[cols]
    out=[]
    for v,l in items:
        if dark: out.append(f'<div class="rounded-xl p-5 sm:p-6 bg-primary-foreground/5 ring-1 ring-primary-foreground/15"><p class="font-display text-4xl font-bold leading-none sm:text-5xl text-accent">{v}</p><p class="mt-3 text-sm leading-snug text-primary-foreground/75">{l}</p></div>')
        else: out.append(f'<div class="rounded-xl p-5 sm:p-6 bg-surface ring-1 ring-border"><p class="font-display text-4xl font-bold leading-none sm:text-5xl text-primary">{v}</p><p class="mt-3 text-sm leading-snug text-foreground/75">{l}</p></div>')
    return f'<div class="my-8 grid gap-4 {g}">'+''.join(out)+'</div>'
def cards(items,cols=3,border='border-accent'):
    g={3:'md:grid-cols-2 lg:grid-cols-3',5:'md:grid-cols-2 lg:grid-cols-5',2:'md:grid-cols-2',4:'md:grid-cols-2 lg:grid-cols-4'}[cols]
    out=[]
    for it in items:
        bd=border
        if isinstance(it,tuple) and len(it)==3: t,x,bd=it
        else: t,x=it
        out.append(f'<div class="rounded-xl border-t-4 {bd} bg-surface p-6 transition-transform hover:-translate-y-0.5 [&amp;_p]:my-0 [&amp;_strong]:mb-2 [&amp;_strong]:block [&amp;_strong]:font-display [&amp;_strong]:text-xl">{p(b(t)+" "+x)}</div>')
    return f'<div class="my-8 grid gap-4 {g}">'+''.join(out)+'</div>'
def numcards(items):
    out=[]
    for i,(t,x,proof) in enumerate(items,1):
        out.append(f'<div class="flex flex-col rounded-xl bg-surface p-6 ring-1 ring-border"><span class="flex h-9 w-9 items-center justify-center rounded-full bg-primary font-display text-sm font-bold text-accent">{i}</span><p class="mt-4 font-display text-xl font-bold leading-snug">{t}</p><p class="mt-3 text-sm leading-relaxed text-foreground/80">{x}</p><p class="mt-auto border-t border-border pt-4 text-xs leading-relaxed text-muted-foreground"><span class="font-bold text-foreground">Proof: </span>{proof}</p></div>')
    return '<div class="my-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">'+''.join(out)+'</div>'
def table(head,rows,boldlast=False):
    th=''.join(f'<th class="px-4 py-3 align-bottom text-xs font-bold tracking-wide uppercase">{x}</th>' for x in head)
    trs=''
    for r in rows:
        trs+='<tr class="even:bg-surface/60">'+''.join(f'<td class="border-t border-border px-4 py-3 align-top leading-snug">{x}</td>' for x in r)+'</tr>'
    return f'<div class="my-6 overflow-x-auto rounded-lg border border-border"><table class="w-full min-w-[560px] border-collapse text-left text-sm"><thead class="bg-primary text-primary-foreground"><tr class="even:bg-surface/60">{th}</tr></thead><tbody>{trs}</tbody></table></div>'
def acc(title,sub,inner):
    return f'<div class="my-3 rounded-xl border border-border bg-background transition-shadow hover:shadow-sm"><button type="button" aria-expanded="true" class="flex w-full items-start justify-between gap-4 px-5 py-4 text-left sm:px-6"><span><span class="block font-semibold text-foreground">{title}</span><span class="mt-1 block text-sm text-muted-foreground">{sub}</span></span>{CHEV}</button><div class="border-t border-border px-5 pb-6 sm:px-6">{inner}</div></div>'
def finding(n,title,found,fix):
    return acc(f'{n}. {title}', f'The fix: {fix}', p(b('What we found:')+' '+found)+p(b('The fix:')+' '+fix))
def fig(cap,sub,inner,dark=False):
    if dark: return f'<figure class="my-10 rounded-2xl p-6 sm:p-8 bg-primary text-primary-foreground"><figcaption class="mb-6"><p class="text-xs font-bold tracking-[0.18em] uppercase text-accent">{cap}</p><p class="mt-1 text-sm text-primary-foreground/65">{sub}</p></figcaption>{inner}</figure>'
    return f'<figure class="my-10 rounded-2xl p-6 sm:p-8 bg-background ring-1 ring-border"><figcaption class="mb-6"><p class="text-xs font-bold tracking-[0.18em] uppercase text-secondary">{cap}</p><p class="mt-1 text-sm text-muted-foreground">{sub}</p></figcaption>{inner}</figure>'
def hbars(rows,maxv=None,fmt=lambda v:str(v)):
    maxv=maxv or max(v for _,v,_ in rows) or 1
    out=[]
    for name,v,me in rows:
        w=0 if v is None else max(0.5,100*v/maxv)
        lab=f'<span class="truncate text-sm font-bold text-foreground">{name}</span>' if me else f'<span class="truncate text-sm text-foreground/75">{name}</span>'
        bc='bg-destructive' if me else 'bg-primary'
        vc='font-bold text-destructive' if me else 'font-semibold'
        out.append(f'<div class="grid grid-cols-[minmax(0,10rem)_1fr] items-center gap-3 sm:grid-cols-[14rem_1fr]">{lab}<div class="flex items-center gap-3"><div class="h-7 flex-1 overflow-hidden rounded-md bg-muted"><div class="h-full rounded-md {bc}" style="width: {w}%"></div></div><span class="w-20 shrink-0 text-right text-sm tabular-nums {vc}">{fmt(v)}</span></div></div>')
    return '<div class="space-y-3">'+''.join(out)+'</div>'
def gauge(score,label):
    C=263.89378290154264; col='text-destructive' if score<50 else ('text-accent' if score<90 else 'text-success')
    off=C*(1-score/100)
    return f'<div class="flex flex-col items-center"><div class="relative h-28 w-28"><svg viewBox="0 0 100 100" class="h-full w-full -rotate-90"><circle cx="50" cy="50" r="42" class="stroke-primary-foreground/15" stroke-width="9" fill="none"></circle><circle cx="50" cy="50" r="42" class="{col}" stroke="currentColor" stroke-width="9" stroke-linecap="round" fill="none" stroke-dasharray="{C}" stroke-dashoffset="{off}"></circle></svg><span class="absolute inset-0 flex items-center justify-center font-display text-3xl font-bold {col}">{score}</span></div><p class="mt-2 text-xs font-semibold tracking-wide text-primary-foreground/70 uppercase">{label}</p></div>'
def darkstat(v,l,sub,bad=True):
    c='text-destructive' if bad else 'text-success'
    return f'<div class="rounded-xl bg-primary-foreground/5 p-4 ring-1 ring-primary-foreground/15"><p class="font-display text-2xl font-bold {c}">{v}</p><p class="text-sm text-primary-foreground/80">{l}</p><p class="mt-1 text-xs text-primary-foreground/55">{sub}</p></div>'
def steps(items,cols=4,arrows=True):
    out=[]
    for i,(t,tag,x) in enumerate(items,1):
        a=ARROW_R_SM if arrows and i<len(items) else ''
        out.append(f'<li class="relative rounded-xl bg-primary p-6 text-primary-foreground"><span class="font-display text-sm font-bold text-accent">{i:02d}</span><p class="mt-2 font-display text-2xl font-bold">{t}</p><p class="mt-2 text-xs font-bold tracking-wide text-accent uppercase">{tag}</p><p class="mt-3 text-sm leading-snug text-primary-foreground/75">{x}</p>{a}</li>')
    return f'<ol class="my-10 grid gap-4 md:grid-cols-{cols}">'+''.join(out)+'</ol>'
def stages(items):
    out=[]
    for i,(t,q,x,today) in enumerate(items,1):
        a=ARROW_R_LG if i<len(items) else ''
        out.append(f'<div class="relative flex flex-col rounded-2xl bg-primary p-7 text-primary-foreground"><span class="font-display text-sm font-bold text-accent">{i:02d}</span><p class="mt-2 font-display text-3xl font-bold">{t}</p><p class="mt-2 text-sm font-semibold text-accent">{q}</p><p class="mt-4 text-sm leading-relaxed text-primary-foreground/75">{x}</p><p class="mt-6 rounded-lg bg-primary-foreground/5 px-3 py-2 text-xs ring-1 ring-primary-foreground/15"><span class="font-bold text-destructive">Today: </span>{today}</p>{a}</div>')
    return '<div class="my-10 grid gap-4 lg:grid-cols-3">'+''.join(out)+'</div>'
def marked(items,note):
    out=[]
    for k,(t,x) in zip('abcdefgh',items):
        out.append(f'<li class="flex gap-3 rounded-xl bg-surface p-5 ring-1 ring-border"><span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-destructive text-xs font-bold text-destructive-foreground">{k}</span><div><p class="font-display font-bold">{t}</p><p class="mt-1 text-sm text-foreground/75">{x}</p></div></li>')
    out.append(f'<li class="flex items-center gap-3 rounded-xl bg-primary p-5 text-sm text-primary-foreground sm:col-span-2">{PHONE}{note}</li>')
    return '<ol class="grid gap-3 sm:grid-cols-2">'+''.join(out)+'</ol>'
def ul(items): return '<ul class="my-4 max-w-3xl list-disc space-y-2 pl-5 marker:text-secondary">'+''.join(f'<li class="leading-relaxed text-foreground/85">{b(t)} {x}</li>' for t,x in items)+'</ul>'
def chips(cls,items): return f'<div class="grid grid-cols-2 gap-2 sm:grid-cols-{len(items) if len(items)<=5 else 5}">'+''.join(f'<div class="rounded-lg px-3 py-3 text-center text-xs font-semibold leading-snug {cls}">{x}</div>' for x in items)+'</div>'
def slot(icon,title,today,items):
    lis=''.join(f'<li class="flex gap-2 text-sm">{CHECK()}{x}</li>' for x in items)
    return f'<div class="flex flex-col rounded-2xl bg-surface p-6 ring-1 ring-border">{icon}<p class="mt-3 font-display text-2xl font-bold">{title}</p><p class="mt-2 text-xs font-semibold text-destructive">Today: {today}</p><ul class="mt-4 space-y-2">{lis}</ul></div>'
