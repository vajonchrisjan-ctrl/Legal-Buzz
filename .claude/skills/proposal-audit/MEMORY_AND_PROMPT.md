# Proposal audit: memory + starter prompt

Paste **Part 1** into a project's memory or custom instructions (claude.ai Project, a new
CLAUDE.md, or the top of a session). Paste **Part 2** as the first message of each new prospect
session, with the blanks filled in. This works even where the repo skill isn't loaded.

---

## Part 1: Memory (the standing logic)

**Purpose:** legalbuzz pitches AI SEO to law firms through a proposal page per prospect
(legalbuzz.co/proposal/<slug>). Before it's presented, every claim gets checked against the
prospect's live website and our SEO data, and the new data goes into a proposal-styled PDF
addendum. One prospect per session.

**Sources of truth, in order**
1. The prospect's live website, read directly. Never trust a dashboard or a proposal number without checking it.
2. SE Ranking exports: AI Search research CSVs, site audit, domain strength (DT) and traffic.
3. DataForSEO / SE Visible AI-answer tests, which the proposal cites.
4. The proposal text. The live page shows dropdown titles only. The full copy is in Lovable
   ("George's Lovable" → project "legalbuzz" → `src/content/<slug>-pitch.md`).

**How to check**
- **Pacing:** pace site requests (about 1.5s apart, never in parallel). Law-firm hosts sit behind bot protection.
- **Get the page list from the sitemap:** posts are articles, practice-area post types are service pages, and pages, locations, team and taxonomies are other.
- **Measure main content only** (exclude menus and footers) for word counts and internal links.
- **For each proposal claim, grade it** ✅ confirmed / ⚠️ partly confirmed or unverifiable / ❌ wrong or self-contradicting, with the evidence.
- **Standard checks:**
  - **Counts:** articles and service pages.
  - **E-E-A-T:** named lawyer authors (schema Person, not testimonials), "reviewed on" dates, credentials, first-hand experience.
  - **Information gain:** real fees (not legal thresholds like "$100,000"), examples, original data, tables, links to the law or regulator.
  - **Out-of-date terms:** e.g. AU "AAT", replaced by the ART on 14 Oct 2024.
  - **Thin and template pages:** batch publishing (many pages within minutes or 24 hours).
  - **Internal linking:** orphan articles, articles linking to services, services linking to articles, and how many articles the news index lists.
  - **Duplicate service pages:** same slug stem, different publish batch, and misspelt slugs.
  - **Schema:** is there LegalService/Organization schema? FAQPage?
  - **Site-wide faults:** PHP errors in the footer (often leaking server paths), animated counters that read "0+" to bots, spam comments (`/wp-json/wp/v2/comments` X-WP-Total), and internal links that redirect, especially from one city to another.
  - **Whether robots.txt blocks AI bots.**
  - **Contact details:** published office addresses per city, and directory listings that disagree with them (NAP consistency).
- **Not checkable without a source:** Google rankings, Google review counts, "trust score", "E-E-A-T %". Mark ⚠️ and ask for the screenshot.

**AI visibility logic**
- **NAMED and CITED are separate measures.** Never mix them in one stat.
  - Named means AI writes the firm's name (e.g. DataForSEO, X of N answers across ChatGPT, Perplexity, Google AI Mode and Claude).
  - Cited means AI links to the firm's site as a source (SE Ranking AI Search: citations by topic and engine).
- **Re-add the per-platform numbers** and check them against the hero stats. Use one total across the whole proposal.
- **Reading the SE Ranking exports:**
  - The topics CSV cells look like "23 (0.18%)". That's citations.
  - Columns that are search engines or government bodies ("Google Search", "Department of …") are not competitors. Leave them out of firm comparisons.
  - Topic labels are auto-generated and US-leaning. Drop off-topic ones, and footnote how many citations were dropped so the totals reconcile.
- **Authority vs reputation:** compare DT and traffic with competitors.
  - If DT is similar but citations are lower, the gap is reputation.
  - Show which third-party sites AI cites next to competitors but not the prospect (Best Lawyers, google.com listings, Law Society, Reddit, YouTube, Facebook, directories).
- **AI Overviews SOP (Jake Ward):** only step 5 ("build something better") can be checked on the site. Steps 1–4 and 6 are the agency's tracking process.
- **Migration lawyers aren't on the MARA register.** Frame it as "explain lawyer vs agent", not "get listed".

**Traps found before (Sambi Legal, Oct 2026), so check them every time**
- The hero stat disagreed with the platform sum (10 vs 11), and several totals were used for one test (500+, 720, 935, 540).
- "98% of mentions from AI Overviews" sat next to a "named" figure, mixing the two measures.
- The same metric got conflicting grades (E-E-A-T 60% vs F, 0 of 43).
- "AI gets you wrong: no Melbourne office" while the site itself published no Melbourne address. Check the site before calling AI wrong.
- The proposal page's own branding for an Australian prospect: a UK 020 number, a "UK law firms" footer, the "SRA Code", and only a UK case study.

**Outputs**
- **Report** in box format: one box per claim, with Result, Live site change, Proposal says and Reality check. Then a Bottom line and a NEXT line.
- **Addendum PDF:** A4, legalbuzz style. Fonts are Outfit (headings) and DM Sans (body). Colours are navy #000d1f, yellow #f5d400, red #e5484d for losses, and ink #050505. Layout follows the proposal: dark cover with stat cards, section eyebrows, red bars for the prospect, yellow "In plain English" boxes and a navy call-to-action.
  - Client-facing only. Internal corrections go to the user in chat.
  - Render with headless Chromium. Check that no page overflows, and look at every page before sending.

**Guardrails**
- Always say whether anything changed on a live site. A read-only check is "No".
- Never edit the live proposal (Lovable, which spends credits and changes a public page) or the prospect's site without an explicit "go".
- Never present a number you didn't verify as verified.
- Don't use the prospect's logo or impersonate them.

---

## Part 2: Starter prompt (one per prospect session)

```
Use the proposal-audit skill (if it isn't loaded, follow the "Proposal audit memory" above).

Prospect: <Firm name>
Proposal: https://legalbuzz.co/proposal/<slug>
Prospect site: https://<domain>/
Attached: <SE Ranking exports: Export_research_external_llm_<Firm>.csv and
Export_research_llm_second_part_for_<Firm>.csv / site audit / none>

1. Read the full proposal (live page + src/content/<slug>-pitch.md in the Lovable "legalbuzz" project, read-only).
2. Download the prospect's site from its sitemap (paced) and run every standard check.
3. Grade each proposal claim ✅ / ⚠️ / ❌ with evidence, one box per claim, plus
   "Could add to the proposal" findings the proposal missed.
4. Summarise the SE Ranking exports: citations vs competitors, engine split, topics won/behind,
   gap topics, authority vs reputation.
5. Build the client-facing AI-citations addendum PDF in the legalbuzz proposal style and send it.
Do not edit the live proposal or the prospect's site. Tell me what you'd change and wait for "go".
```

**Follow-up prompts**
- `Recheck <slug> against the live site again. Only report what changed since the last check.`
- `Apply the ❌ fixes to src/content/<slug>-pitch.md in Lovable. Go.` (only when you're ready for it to go live)
- `Draft replacement wording for every ⚠️/❌ line.`
