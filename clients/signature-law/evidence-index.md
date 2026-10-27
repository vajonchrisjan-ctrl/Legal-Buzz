# Signature Law — Evidence Index (Round 1)

All checks below were run against the live site and public registers on **27 Oct 2026**
(UTC; Bowral is AEDT/UTC+11, so local collection time is 28 Oct 2026 early morning).
Status vocabulary per master prompt §0.4: *newly measured / reused historical / not supported /
failed / not applicable / awaiting client confirmation*.

**No chargeable action was taken. No account was created. No tracker project was created.
Nothing on the site or on any listing was changed.** This round is entirely read-only.

## Status counts

| Status | Checks |
|---|---|
| Newly measured | 14 |
| Not supported (tool not available this session) | 6 |
| Failed (blocked / quota) | 2 |
| Awaiting client confirmation | 9 (listed in §C) |

---

## A. Checks completed — newly measured

| ID | Check | Tool / module | Exact setting | Collected (UTC) | Status | Rows OK / failed |
|---|---|---|---|---|---|---|
| A1 | robots.txt | curl | direct fetch | 2026-10-27 13:35 | newly measured | 1/0 |
| A2 | /llms.txt | curl | direct fetch | 2026-10-27 13:35 | newly measured — **HTTP 404, file absent** | 1/0 |
| A3 | Sitemap index + 4 child sitemaps | curl | Yoast sitemaps | 2026-10-27 13:35 | newly measured | 5/0 |
| A4 | Full page crawl — 46 URLs | Python+bs4, 1 req/sec | desktop UA, served HTML | 2026-10-27 13:36–13:38 | newly measured | 46/0 (1 transient proxy error, retried OK) |
| A5 | Rendered-DOM check (homepage) | Playwright/Chromium | networkidle + 3s wait | 2026-10-27 13:41 | newly measured | 1/0 |
| A6 | Host canonicalisation (8 variants) | curl | http/https, www, trailing slash, UPPERCASE, /index.html, bogus URL, wp-json/users | 2026-10-27 13:43 | newly measured | 8/0 |
| A7 | Lighthouse — homepage, **mobile** | Lighthouse 12.2.1, local Chromium | formFactor mobile, 412×823, simulate, 4× CPU, 150ms RTT, 1638.4 Kbps | 2026-10-27 13:47 | newly measured | 1/0 |
| A8 | Lighthouse — homepage, **desktop** | Lighthouse 12.2.1 | desktop preset, 1350×940, 1× CPU, 40ms RTT, 10240 Kbps | 2026-10-27 13:45 | newly measured | 1/0 |
| A9 | Lighthouse — /property-law-and-conveyancing/, mobile + desktop | Lighthouse 12.2.1 | as above | 2026-10-27 13:47 | newly measured | 2/0 |
| A10 | Company register — ABN lookup | ABR (abr.business.gov.au) | search "signature law", then ABN detail view | 2026-10-27 13:44 | newly measured | 13/0 |
| A11 | Security + cache headers | curl -D | homepage response headers | 2026-10-27 13:52 | newly measured | 1/0 |
| A12 | Image content negotiation | curl, `Accept: image/webp` | logo asset on i0.wp.com | 2026-10-27 13:52 | newly measured | 1/0 |
| A13 | Directory listing — Localsearch | page read in full | live profile page | 2026-10-27 13:49 | newly measured | 1/0 |
| A14 | Directory listing — LawTap (firm + principal) | page read in full | live profile page | 2026-10-27 13:49 | newly measured | 2/0 |
| A15 | LinkedIn company page | page read in full | au.linkedin.com/company/signaturelaw | 2026-10-27 13:51 | newly measured | 1/0 |

## B. Checks NOT completed — and exactly why

| ID | Check (master prompt §) | Status | Reason |
|---|---|---|---|
| B1 | Rankings, 10 phrases × location × device, depth 100 (§2C) | **not supported** | No rank tracker available in this session. SE Ranking / Search Atlas / Semrush / Ahrefs are not connected (each requires OAuth the session cannot start). Direct scripted Google fetches are forbidden by §2C and would 403 regardless. **No rank figure of any kind is reported.** |
| B2 | Keyword demand / volumes (§2D) | **not supported** | Same — no keyword tool connected. **No volume is estimated or inferred.** Missing ≠ zero. |
| B3 | Traffic distribution, keyword × domain (§2E) | **not supported** | *Compatible keyword-level cross-domain traffic data unavailable.* No domain-level figure has been substituted, per §2E. |
| B4 | AI visibility, 8 questions × 6 platforms (§2F) | **not supported** | No neutral research account is available for ChatGPT, Gemini, Perplexity, Google AI Overview or AI Mode in this session. Per §2F, using a personalised signed-in account for neutral research is not acceptable, and this assistant's own output is not a measurement of a consumer platform. **No mention rate is reported.** |
| B5 | Backlinks, two-tool comparison (§2I) | **not supported** | Neither SE Ranking Backlink Checker nor Search Atlas Site Explorer is connected. No link or domain count is reported. |
| B6 | Google Business Profile / Maps fields + grid (§2G) | **failed (partial)** | Searched by brand name, principal's name, address and both registered business names. No GBP profile surfaced through the routes available here, and Maps cannot be queried directly from this session. Per §2G, **this is NOT a finding that no listing exists** — it is an unverified check. Must be confirmed by someone signed in to Maps/GBP. |
| B7 | PageSpeed Insights (§2B) | **failed** | PSI API returned HTTP 429, "Quota exceeded … Queries per day", on all 4 runs at 13:45 UTC. The PSI browser UI was then tried as §2B directs and hung on "Running analysis" (same backend quota). **Substituted with local Lighthouse 12.2.1 using the mobile preset with simulated throttling (4× CPU, 150ms RTT, 1638.4 Kbps)** — this is the throttled mobile profile, not a raw unthrottled headless run. Labelled as local Lighthouse, not PSI, everywhere. CrUX field data: **not collected** (CrUX API needs a key) — field performance is therefore unknown, not "No Data". |
| B8 | The Fold directory listing (§2H) | **failed** | Page returned a "Bot Verification" interstitial. Per §2H: **not verified** — no mismatch is asserted. |
| B9 | Citations across 15–20 directories (§2H) | **partial** | 3 of the target 15–20 read in full (Localsearch, LawTap ×2, LinkedIn). The remainder was not attempted this round. |

## C. Client confirmations required (list only — not answered, per §2J)

1. **Does the firm trade from Moss Vale?** LinkedIn lists a second office at 348–354 Argyle Street, Moss Vale NSW 2577. The website names only Bowral, on every page.
2. **The HR Brief** — registered business name since 26 Jun 2024 against the firm's own ABN. Is it trading? Does it have a site? Is it meant to be public?
3. Which of the two registered business names should carry the online presence — one brand or two.
4. The firm's **founding date**: ABR says ABN active 31 Aug 2015; LinkedIn says founded 2016; Localsearch says "Trading for 10 years". None is asserted as wrong; the client confirms which is correct before any "since" claim is made more prominent.
5. **Ownership of every directory listing** — Localsearch is currently **unclaimed**.
6. Headcount: the About page names 9 people; LinkedIn says 2–10 (5 discoverable); LawTap says "1 Solicitor".
7. Practising certificate / Law Society NSW details and the professional indemnity scheme — the site carries the Professional Standards Legislation line but no registration numbers.
8. Whether anyone has ever bought links or guest posts (asked as a standing question; **no link data was collected this round, so nothing is alleged**).
9. An authorised contact and a confirmed centre point before any Maps grid/heatmap is run (chargeable — would be declared first).

## D. Namesakes — excluded from every count

| Name | Why excluded |
|---|---|
| **signaturelaw.co.uk** | A **UK** firm. Its Trustpilot page carries strongly negative reviews. **These are not the client's** and must never be attributed to the Bowral practice. This is the single highest-risk namesake. |
| SIGNATURE (ABN 78 981 385 133, QLD 4352); SIGNATURE (22 057 746 406, NSW 2044); SIGNATURE & CO PTY LTD (34 696 991 278); SIGNATURE CO PTY LTD (89 674 829 077); SIGNATURA CO PTY LTD; LA SIGNATURE PTY LTD; LA Signature Studio; SOGNATORE; SIGNATORRA; Le Signature; SIGNATIVE | Separate ABNs, not the client. Returned by the same register search. |
| hrbrief.com.au | Read in full: a Ghost-published weekly HR/IR newsletter. No lawyer, no ABN, no Bowral or Signature Law mention. **Not connected to the client's "The HR Brief" business name** on the evidence available. |
| Elizabeth Kenny (Wikipedia) | Historical Australian bush nurse. Unrelated to the principal of the same name. |

## E. Corrections to our own work

None yet — this is round 1 and no earlier figures exist for this client. Any later round that
contradicts the above replaces it here, visibly, per §3.

## F. Proposal build record (round 1)

Deliverable: `Signature-Law-Growth-Proposal-legalbuzz.pdf` — 18 A4 pages, 11 numbered sections.
Source and build scripts: `clients/signature-law/proposal/` (`build.sh` assembles, renders, and measures page fill).

Decisions taken by the user for this build:
- Build on technical evidence only; rankings, volumes, traffic share, AI visibility and backlinks shown as *Not measured*.
- Treat Signature Law Bowral as a single brand; Moss Vale and The HR Brief carried as open questions, with the
  architecture recommendation (Option A) stated as conditional on Moss Vale not trading.

Checks run on the PDF itself:
- Fonts: Outfit and DM Sans embedded base64; canvas widths differ from the serif fallback (398 / 405 vs 367).
- Contents page numbers computed from the rendered PDF and re-verified after substitution: 11 of 11 match.
- Pagination: first draft used fixed A4 boxes and silently clipped content on 13 of 17 pages (up to 773 px on the
  action-plan page). Rebuilt as a flowing layout; no page below 32% fill except the cover and the final page.
- Chart palette (navy / blue / red) tested under Machado protan / deutan / tritan simulation: every pair ΔE ≥ 55.
- Overall score: 7+5+4+4+3+2+2+2+0 = 29 of 90 = 32.2, shown as 32/100. This is a legalbuzz assessment, not an index.

Drafting corrections made before delivery (no figure had been issued to the client):
- Blog posts since 2024: draft said 2; sitemap shows **3** (two Nov 2024, one Jul 2026).
- "Nine named practitioners with bios": only some bios were read in full; now "nine named team members".
- Stacks Law Firm "part of a multi-office network": not verified; removed.
- "Several competitors market by town": only KQ Lawyers and Our Lawyers were shown naming other towns; reworded to "at least two", from search results.
- The first contents check reported "consistent" while content was being clipped; the check was meaningless until the layout was fixed.

## G. Design alignment to the live legalbuzz proposal (round 1, second pass)

The proposal was restyled to match https://legalbuzz.co/proposal/thynne-macartney. That page sits behind a
"Confirm who's reading" name/email gate; **the gate was not submitted**. Design tokens and component styles were
read from the page's published stylesheet and computed DOM styles only.

Where the live page differs from the design spec in the master prompt, the live page was followed:

| Element | Master-prompt spec | Live page (followed) |
|---|---|---|
| Section opener | Dark navy block, faded numeral, yellow kicker | White page; navy badge with yellow number + caps label; very large black Outfit headline |
| Key takeaway | Dark navy card | Yellow (#f5d400) rounded callout |
| Radii | 12px cards | 4px tables, 8px cards, 12px callouts/figures, 16px feature cards, full pills |
| Table header | Outfit caps, 0.11em tracking | DM Sans bold caps, tight tracking; bordered 4px wrapper; even rows surface/60 |
| Sub-headings | Yellow left rule | Plain Outfit bold |
| Cover | Score card with large red /100 | Firm name + yellow kicker, tagline, three cards, evidence-source pills, numbered contents pills |
| Contents | Table | Numbered cards |
| Six-month plan | Pills in a table | Yellow cell grid (solid = focus, 45% = active, light = maintain) |

The overall 32/100 score moved from the cover into Section 5, where the live page keeps its scores.
Cover tagline "Be seen. Be trusted. Be chosen." is taken from the live page's cover.

Re-verified after the restyle: 18 pages; contents page numbers 11 of 11 match the rendered PDF; no page below
32% fill except one coherent section-ending table (28%) and the last page; 33 content checks all present.
