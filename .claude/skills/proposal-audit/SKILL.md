---
name: proposal-audit
description: Verify a legalbuzz growth proposal (legalbuzz.co/proposal/<firm>) claim by claim against the prospect law firm's live website and SE Ranking AI-search exports, then build a client-ready AI-citations addendum PDF styled like the proposal. Use when the user shares a legalbuzz proposal link or screenshot, asks to "recheck the data", "cross-reference the proposal with the site", checks a prospect's AI presence / AI Overviews / authority vs reputation, or uploads SE Ranking "Export_research_*llm*" CSVs.
---

# Proposal audit (one prospect per session)

legalbuzz pitches AI SEO to law firms using a proposal page per prospect. Before it goes to
the firm, every number on it must be checked against the firm's live site, because a wrong
claim in the room loses the deal. This skill is the method used for Sambi Legal (Oct 2026);
`templates/addendum-example-sambi.html` is the finished worked example.

Run everything from the session scratchpad. Pace all requests to the prospect's site
(`PACE` env, default 1.5s); law-firm hosts often sit behind SiteGround/Cloudflare bot protection.

## Inputs to ask for (if missing)
1. Proposal URL, e.g. `https://legalbuzz.co/proposal/<slug>`. A screenshot is not enough:
   full-page screenshots are unreadable. Ask for the link.
2. Prospect domain.
3. Optional: SE Ranking AI Search > Research exports. There are two CSVs:
   `Export_research_external_llm_<Firm>_<Month>.csv` (topics) and
   `Export_research_llm_second_part_for_<Firm>.csv` (cited domains).

## Workflow
1. **Get the proposal text.** Run `python3 scripts/extract_proposal.py <url> proposal.txt` and read all of it.
   - Collapsed dropdowns only show their titles on the live page.
   - The full copy lives in Lovable workspace "George's Lovable", project **legalbuzz**
     (`a530b57c-7f5e-491b-8904-f66e3d10c927`), at `src/content/<slug>-pitch.md`.
     The route is `src/routes/proposal.<slug>.tsx`, and a `-v2` sales-flow version may exist too.
   - Read it with `mcp__Lovable__read_file`. Delegate the reading to a subagent, because the file runs to about 2,000+ lines.
2. **Download the site.** Run `bash scripts/fetch_site.sh <domain> work`.
   - Then fix `work/list.txt` by hand:
     - Hub or service pages that sit in `page-sitemap` are tagged `O`. Retag them as `S`.
     - Add team pages as `O` lines, so lawyer names get detected.
3. **Measure.** Run `python3 scripts/site_checks.py work <domain> --live`. It prints 11 numbered blocks covering:
   - page counts
   - authorship and E-E-A-T
   - information gain (fees, law links, tables)
   - out-of-date terms
   - thin pages
   - publishing batches
   - internal linking
   - duplicates and canonicals
   - schema
   - site-wide errors (PHP errors, animated "0+" counters, robots)
   - live probes (spam comment count, redirecting internal links)
4. **Summarise the SE Ranking exports**, if supplied. Run `python3 scripts/seranking_ai.py topics.csv domains.csv <domain>`.
5. **Check each proposal claim** against steps 3 and 4. Grade every claim as one of:
   - ✅ confirmed (exact or within rounding)
   - ⚠️ partly confirmed, unverifiable, or a weak number
   - ❌ wrong, or the proposal contradicts itself
6. **Report** in the CLAUDE.md multi-item box format. Say plainly that nothing on the live site or the live proposal was changed.
7. **Build the addendum PDF** if asked:
   - Copy `templates/addendum-example-sambi.html`.
   - Replace the firm, figures, topics and competitors.
   - Run `PLAYWRIGHT=$(npm root -g)/playwright node scripts/render_pdf.js in.html out.pdf`.
   - Fix any page the table flags as `OVERFLOW`.
   - Rasterise with `pdftoppm -r 70 -png` and look at every page.
   - Send it with SendUserFile.

## Claims proposals usually make, and how to verify them
| Proposal claim | Where to check |
|---|---|
| "N articles and N service pages" | site_checks block 1 (sitemap-based) |
| Named lawyer or author 0 of N | block 2: schema Person and team-name hits. Read the context: names usually appear only in testimonials |
| "Reviewed on" date, fees, first-hand experience | block 2/3. "$100,000" is often a legal threshold, not a fee. "Reviewed by" is often "decisions are reviewed by a tribunal" |
| Links to the law or regulator: N (x articles, y services) | block 3 |
| Out-of-date tribunal names (AU: AAT→ART, Oct 2024) | block 4. Edit the regex for UK or other jurisdictions |
| Thin or template articles, "published within minutes" | blocks 5–6 |
| Orphan pages, "articles link to the service", news index shows 12 | block 7. SE Ranking counts orphans site-wide (menus and news index included), so its number is lower than the main-content-only count |
| Duplicate pairs, canonicals fine | block 8. Confirm each pair by reading it, and compare publish months (Feb vs May batches) |
| "No page tells Google you're a law firm" | block 9 |
| "Error on every page", "0+ counters", "N spam comments" | blocks 10–11. Comment counts grow, so quote the current figure |
| Redirecting internal links | block 11. Note when a link sends one city's page to another city |
| Google rankings, review counts, "trust score", "E-E-A-T %" | Not checkable from here (WebSearch is US-only). Mark ⚠️ and ask for the source screenshot |
| AI answer percentages | Re-add the per-platform numbers and compare them with the hero stats (see below) |

## Lessons from Sambi (check these every time)
- **"Named" and "cited" are different measures, and proposals mix them up.**
  - Named means AI writes the firm's name (DataForSEO; Sambi: 11 of 720 answers).
  - Cited means AI links to the firm's site as a source (SE Ranking; Sambi: 102, of which 99 were in AI Overview topics).
  - A hero stat like "10 naming Sambi" next to "98% of mentions from AI Overviews" contradicts itself. Report them as two separate rows.
- **Re-add the platform numbers.** The Sambi hero said 10, but the platforms summed to 11, and the totals of 500+, 720, 935 and 540 were all used for the same test.
- **"AI gets you wrong" claims can backfire.** Example: "AI says no Melbourne office" while the site itself publishes no Melbourne address. Check the site before calling AI wrong. Make it a fix item, and ask the firm to confirm the fact.
- **Inconsistent grades.** For example, "E-E-A-T 60%" in one section and "F, 0 of 43" in another.
- **The proposal page's own branding.** It uses a UK 020 number, a footer reading "UK law firms" and the "SRA Code" while pitching an Australian firm. Flag this every time.
- **Competitor columns in the SE Ranking exports.** Columns like "Google Search" or "Department of Home Affairs" are not firms. `seranking_ai.py` excludes them from firm comparisons.
- **SE Ranking topic labels are auto-generated and US-leaning** ("Player Rankings", "Green Card"). Exclude off-topic ones (tune `--off`), and say in a footnote how many citations were excluded so the totals still reconcile.
- **Authority vs reputation framing.** Compare domain strength (DT) with competitors.
  - If DT is similar but citations are lower, the gap is reputation.
  - Look at which third-party sites AI cites next to competitors (Best Lawyers, google.com listings, Law Society, Reddit, YouTube, Facebook).
- **Migration lawyers are not on the MARA register.** Turn that into "explain lawyer vs agent", not "get listed".
- **NDIS / ART timeframes in AU proposals.**
  - Internal review: within 3 months. The NDIA aims to decide in 60 days and must within 90.
  - The ART: within 28 days.
  - Federal Court: within 28 days, on a question of law only.
  - Have a lawyer sign off on these anyway.

## Guardrails
- **Never edit the live proposal or the prospect's site without an explicit "go".** Editing the Lovable project changes a public page and spends the workspace's Lovable credits. Offer it instead.
- The PDF is client-facing. Internal corrections (contradictions, branding problems) go to the user in chat, not into the PDF.
- Don't copy the prospect's logo or impersonate them. Use their name in text only.
- Keep separate sessions per prospect, as the user prefers. Keep the work dir and outputs in that session's scratchpad.
