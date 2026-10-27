# Signature Law (signaturelaw.com.au) — Round 1 findings

Measured 27 Oct 2026 UTC. Every figure here comes from this client's own site, the ABR,
or a listing page read in full. Nothing is carried over from another client.
Scope limits and unmeasured items: see `evidence-index.md` §B.

---

## 1. Identity (master prompt §1)

| Field | Value | Source |
|---|---|---|
| Entity name | **SIGNATURE LAW PTY LTD** | ABR |
| ABN | **48 607 957 291** | ABR |
| ACN | 607 957 291 | ABR |
| Status | Active from **31 Aug 2015** | ABR |
| Entity type | Australian Private Company | ABR |
| GST | Registered from 31 Aug 2015 | ABR |
| Main location | NSW **2576** (Bowral) | ABR |
| Registered business name | **Signature Law** — from **14 Oct 2022** | ABR |
| Registered business name | **The HR Brief** — from **26 Jun 2024** | ABR |
| Principal | Elizabeth Kenny | About page |
| Office (site) | 49 Bowral Street, Bowral NSW 2576 | Contact page |
| Postal | PO Box 1566, Bowral NSW 2576 | Contact page |
| Office (LinkedIn only) | **348–354 Argyle Street, Moss Vale NSW 2577** | LinkedIn |
| Phone | 02 4861 2345 (plus mobile 0493 064 385 on contact page) | Contact page |
| Email | administration@signaturelaw.com.au | rendered DOM |
| Web vendor | Outshine Online | footer |

**No ABN is displayed anywhere on the website** — checked across all 46 crawled URLs.
§1.1 asks us to verify using the number shown on the site; there is none, so the entity was
matched by name + postcode and the match is unambiguous (only one "Signature Law" at 2576).

**Two identity issues carry into the proposal:**
- **A second office with no web presence.** LinkedIn lists Moss Vale; the site never mentions it.
  If the firm trades there, it currently has no page, no NAP and no local signal for that town.
- **A second registered brand with no web presence.** "The HR Brief" has been registered since
  Jun 2024. `hrbrief.com.au` was read in full and is an unrelated Ghost newsletter.

**Founding-date discrepancy (do not resolve — client confirms):**
ABR 31 Aug 2015 · LinkedIn "Founded 2016" · Localsearch "Trading for 10 years".

---

## 2. On-page — the dominant finding

Crawl of all 46 indexable URLs (11 pages, 34 posts, 1 category), served HTML:

| Defect | Count | Note |
|---|---|---|
| **Pages with no meta description** | **45 / 46** | Only the homepage has one (130 chars). Lighthouse fails the service pages on this audit. |
| Pages with no `<h1>` | 2 / 46 | The **homepage** and the category archive. |
| **Pages with no `<h2>` at all** | **46 / 46** | The theme jumps H1 → H3 sitewide. The homepage has neither H1 nor H2. |
| Pages with no `og:image` | 13 / 46 | Includes **every one of the 11 main pages**. Every share of a service page renders imageless. |
| Twitter card beyond `twitter:card` | 0 / 46 | `summary` only, no title/description/image. |
| **Pages with a `tel:` link** | **0 / 46** | The phone number is plain text everywhere, including the contact page. Not tappable on mobile. |
| Pages under 300 words | 3 / 46 | /contact-us/ 224, /litigation/ 266, /practice-areas/ 294. |

Thinnest service pages: **Litigation 266 words**, Workplace Health & Safety 314,
Business & Contract Law 381, Property Law & Conveyancing 492.

Titles are present and reasonable on all 46 (20–51 chars on the main pages).

### Structured data
Yoast default graph only: `WebPage`, `WebSite`, `Organization`, `BreadcrumbList`, `ImageObject`.
Verified identical in served HTML and after full render.
**The `Organization` node carries no address, no telephone, no geo, no opening hours and no
`areaServed`**, and the firm is not typed as `LegalService` / `Attorney`. `sameAs` lists Facebook,
Instagram and LinkedIn. For a single-town practice this is the biggest structured-data gap.

### Analytics — nothing is installed
Checked twice (served HTML and rendered DOM, with network capture over 60 requests):
no GA4, no `gtag`, no `dataLayer`, no GTM container, no Meta Pixel, no LinkedIn tag,
no Hotjar, no Clarity, no legacy UA. The only beacon is Cloudflare Insights.
**The firm currently has no measurement of any kind on its website**, so no enquiry,
call or form submission is attributable today. This bounds what any "before" baseline can show.

---

## 3. Speed — desktop is fine, mobile is not

Local **Lighthouse 12.2.1** (PSI quota was exhausted — see evidence-index §B7).
Mobile = simulated throttling, 4× CPU, 150 ms RTT, 1638.4 Kbps. **These are lab figures,
not CrUX field data; field performance was not collected and is unknown.**

| Page | Form factor | Perf | LCP | TBT | CLS | SI | A11y | BP | SEO |
|---|---|---|---|---|---|---|---|---|---|
| Homepage | **mobile** | **67** | **4.2 s** | 510 ms | 0.018 | 5.1 s | 85 | 79 | 85 |
| Homepage | desktop | 93 | 1.3 s | 10 ms | 0.014 | 1.8 s | 85 | 78 | 85 |
| Property & Conveyancing | **mobile** | **53** | **6.1 s** | 540 ms | 0.114 | 4.8 s | 87 | 79 | 85 |
| Property & Conveyancing | desktop | 96 | 1.1 s | 0 ms | 0.005 | 1.4 s | 87 | 78 | 85 |

The money page is the slowest page on mobile: **LCP 6.1 s** against a 2.5 s good threshold.
Reading the desktop 1.1 s as the real number is exactly the error §2B warns about.

Lab opportunities (mobile homepage): unused JavaScript 328 KB, unused CSS 53 KB / 370 ms,
offscreen images 131 KB, improperly sized images 52 KB.

Failing audits: 6 links with no discernible name (a11y + SEO), 1 non-crawlable link,
10 colour-contrast failures, links distinguishable by colour alone.

**Image delivery is already good** — Jetpack's `i0.wp.com` CDN serves WebP on
`Accept: image/webp` with `vary: Accept` and a 2-year cache. Don't bill for fixing it.

---

## 4. Technical hygiene

Correct: `http→https`, `www→non-www`, missing trailing slash → 301; bogus URL and
`/index.html` both 404; `wp-json/wp/v2/users` returns 401 (user enumeration blocked);
`robots.txt` clean with sitemap declared; canonical, `lang="en-AU"` and viewport on every page.

| Issue | Severity |
|---|---|
| `/ABOUT-US/` (uppercase) returns **200**, not 301 | Low — canonical correctly points to the lowercase URL, so the duplicate is neutralised |
| **No `/llms.txt`** (HTTP 404) | Relevant to AI-surface work |
| **No firm privacy policy anywhere on the site** | The only privacy link is Google's, via reCAPTCHA. Notable for a firm doing conveyancing |
| No HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy | Low SEO impact, trust/security point |
| Footer reads "Copyright 2020" | Staleness signal, 6 years old |
| No practising certificate or Law Society NSW number shown | Trust signal. The Professional Standards Legislation line *is* present |

---

## 5. Off-site — what was actually verified

| Property | State | Read in full |
|---|---|---|
| LinkedIn (`/company/signaturelaw`) | Law Practice, 2–10 staff, founded 2016, 58 followers, **two offices incl. Moss Vale** | yes |
| Localsearch | **Unclaimed.** Phone hidden behind "Show Number". **0 reviews.** Website given as `http://www.signaturelaw.com.au`. "Trading for 10 years" | yes |
| LawTap (firm) | Address + phone correct. **"No lawyers found", FAQ says "1 Solicitor"** — the About page names 9 people. Badly stale | yes |
| LawTap (Elizabeth Kenny) | Principal profile exists | yes |
| Facebook `/signaturelawbowral` | "Not yet rated", 2 reviews | search result only — **not read in full** |
| The Fold | **Bot Verification interstitial — not verified.** No mismatch asserted | no |
| **Google Business Profile** | **Not verified.** Searched by brand, principal, address and both registered names; nothing surfaced through the routes available here. Per §2G this is *not* evidence that no listing exists | no |

**Review position, stated to scope:** across the listings actually read, the firm shows
**0 reviews on Localsearch, none on LawTap, and Facebook "not yet rated"**. No claim is made
about Google reviews, because the Google profile was never verified.

**Competitors — discovered, not preassigned, and not yet verified from their own sites:**
Stacks Law Firm (1/10 Boolwey St, Bowral) · Highlander Law / hlaw.au (Suite 7F, 295 Bong Bong St)
· Oxley Law (11/11–13 Bundaroo St) · KQ Lawyers · Highlands Legal Centre · Our Lawyers (Mittagong)
· Bowral Conveyancing Centre (conveyancing only). **No competitor weakness is claimed** — none
has been measured.

---

## 6. What this means for the proposal

The one decision the proposal turns on: **is this one brand in one town, or a two-office
(Bowral + Moss Vale) and possibly two-brand (Signature Law + The HR Brief) business?**
Everything in the architecture section depends on the answer, and only the client has it.

Highest-value fixes, in order, on evidence actually collected:
1. **Install GA4 + Search Console.** Nothing is measured today; without this there is no baseline.
2. **Meta descriptions on 45 pages**, starting with the 6 service pages.
3. **An H1 on the homepage**, and H2s for section headings sitewide.
4. **`tel:` links** on every phone number — a single-town firm with no tappable number.
5. **`LegalService` schema** with address, phone, geo, hours and `areaServed`.
6. **Mobile LCP on the service pages** (6.1 s on the conveyancing page).
7. `og:image` on the 11 main pages.
8. Claim the Localsearch listing; correct LawTap.
