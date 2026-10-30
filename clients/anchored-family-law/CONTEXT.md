# Anchored Family Law — project context

Consolidated from the earlier "Anchored Family Law website" session (21–30 Oct 2026) so all
Anchored work continues in one session. Nothing here is a live-site change record unless it
says so explicitly.

## The client
- Live site: https://anchoredfamilylaw.com.au/ — WordPress + Elementor Pro.
- Scale: 26 pages, 18 blog posts, 102 images, 11 categories.
- Key plugins: WooCommerce, Calendly bookings, Rank Math (SEO), Elementor Pro, JetEngine,
  Site Kit by Google.
- Contact at the firm: **Emma** — holds the logins, self-describes as limited on platform skills.

## Current project: rebuild onto Kinsta
- Staging: `https://stg-reviewitco-staging.kinsta.cloud` — confirmed 30 Oct as the Anchored
  staging site (MCP server self-identifies as "AI Engine - Anchored Family Law",
  `mcp_ping` returns site name "Anchored Family Law"). The hostname does not say "Anchored",
  which caused an earlier identification doubt — now resolved.
- Staging is correctly `noindex, nofollow`.
- Chosen approach: re-skin on a clone, not a rebuild from scratch.

### Agreed timeline (as last delivered to the boss)
- **WordPress on Kinsta: 5 working days**, Mon 26 → Fri 30 Oct, live Friday.
- **Lovable: 6 working days**, Mon 26 Oct → Mon 2 Nov.
- Presented as a neutral comparison, not a recommendation: the gap is risk, not time.
- Assumes two people, design signed off day 2, content copied as-is, one review round.
- Infographic artifact: https://claude.ai/artifact/FEqGm69m9RAQcbDLiNyn6U (private — must be
  shared from the page's Share menu before the boss can open it).
- PDF version was generated and sent in the earlier session.
- Deferred post-launch to Mon 2 / Tue 3 Nov: meta description fixes, missing OG tags, thin pages.
  Only template-level fixes (e.g. H1s) were inside the 5 days.
- Risk noted: Melbourne Cup Day (Tue 3 Nov) if the team is in Victoria.

### DNS cutover (from Emma's VentraIP screenshot, 28 Oct)
- DNS is managed by **VentraIP**. Exactly one record changes at go-live:
  the root `anchoredfamilylaw.com.au` **A record**, currently `43.250.140.17`, to Kinsta's IP
  (shown in MyKinsta under Sites > Domains after adding the domain).
- `www` is a CNAME to the root, so it follows automatically.
- **Do not touch:** MX (Outlook), SPF/DKIM/DMARC TXT, Google site verification, SendGrid CNAMEs,
  `booking` (proxy.uprintful.com), `mail`, NS records.
- Pre-launch: ask Emma to drop that A record's TTL from 14400 to 300 about a day before.
- Pre-launch check: confirm there is no AAAA record on the root domain.
- Draft email to Emma was written and is in the earlier session's history.

## On-page audit of the LIVE site (21 Oct 2026, read-only — no changes made)
Same technical scope as the JP Goldman work. Counts are from the live site, not staging.

**ISSUE 1 — Missing H1 (the main problem)**
- 20 of 26 pages have no H1. Only `/`, `/map-session-terms/`, `/additional-fees/`,
  `/thank-you/`, `/my-account/` have one.
- Missing on every page that matters: `/services/`, `/parenting-child-custody/`,
  `/property-and-financial/`, `/divorce/`, `/child-support/`, `/pricing/`, `/about/`, `/faq/`,
  `/contact-us/`, `/bookings/`, `/new-client-pathway/`, `/anchoredblog/`, `/join-the-team/`,
  `/resources-hub/`, `/media/`, `/links/`, `/price-list/`.
- Likely cause: Elementor headings set to H2 or a div rather than H1.

**ISSUE 2 — Meta descriptions out of range**
- Too short (<~70 chars): `/media/` 20, `/pricing/` 31, `/map-session-terms/` 37,
  `/resources-hub/` 49, `/bookings/` 60, `/price-list/` 63, `/parenting-child-custody/` 65.
- Too long (>~160 chars): `/` 321, `/faq/` 237, `/about/` 206, `/anchoredblog/` 182.
- `/sitemap/` has none, but is noindex — ignore.

**ISSUE 3 — Incomplete OG/Twitter tags**
- Roughly half the pages carry 7 OG tags, the rest 13. The 7-tag pages most likely lack
  `og:image`, and that includes all four practice-area pages. Needs a per-tag check to confirm.

**ISSUE 4 — Thin content**
- `/resources-hub/` ~18 words, `/price-list/` ~20, `/contact-us/` ~70, `/links/` ~84,
  `/media/` ~85. Counts include nav text, so real body copy is shorter still.

**Correct already**
- Every page has a title tag and a canonical URL.
- Thank-you pages, terms, privacy policy, sitemap and my-account are properly noindex.

## Access
- Staging MCP endpoint: `https://stg-reviewitco-staging.kinsta.cloud/wp-json/mcp/v1/http`
  (HTTP transport, Bearer token). Token was given in chat and is deliberately NOT stored here.
  It is a full-admin credential (create/delete users, delete posts, update options) — rotate it
  once the build is finished.
- Added to this container with `claude mcp add` (project scope, `/root/.claude.json`). Container
  is ephemeral, so it needs re-adding in a new session; MCP servers only load at session start,
  so the tools appear from the next session onward.
- WPVibe currently has only JP Goldman connected — not Anchored.

## Open questions carried over
- Go-live day, now that the original Fri 30 Oct target has arrived.
- Whether Emma agreed to temporary VentraIP access or a call for the DNS change.
- Who at Anchored will make WordPress edits after launch.
- Where the pre-migration ranking baseline is kept.
- Whether Anchored is a tracked Legalbuzz client with a dashboard task board (JP Goldman has one;
  no Anchored tracker link has been provided).

## Staging QA — run 30 Oct 2026
Full report: `staging-qa-report-2026-10-30.html` (published as a private artifact:
https://claude.ai/artifact/DtsQ1kxxBVs8NtHzsrzB51). Read-only run; no site changes made.

- Staging is an **unmodified clone of live** (99.6% identical homepage HTML, same themes
  `hello-elementor` + `stoke`, 44/44 URLs identical on title/description/H1/robots/OG/word count).
  The redesign is NOT on staging yet — repeat QA once it is.
- Before go-live: staging host baked into canonicals/sitemap/Rank Math redirects; reCAPTCHA
  rejects the staging domain (forms untested); Stripe off + Cart/Checkout are drafts (404 on live
  too) while product pages show Add to cart; Calendly `still-not-sure-…` links 404 on 6 pages.
- Inherited from live: 17 indexable pages with no H1, Rank Math Schema module off (0 JSON-LD),
  Poppins font blocked by `http://` URLs in `poppins.css`, Redirections module off with a
  /blog <-> /knowledgebase loop stored, Reddit pixel `a2_imh06ff977eq`, 5 administrator accounts.
- Not tested: form submissions/email, payments, Calendly booking, logins, backup/restore, DNS/SSL
  cutover, Lighthouse/WCAG/cross-browser, content proofreading.
