# JP Goldman — SEO Work scope (current focus)

Client: JP Goldman (https://www.jpgoldman.co.uk/), tracked in the Legalbuzz dashboard at:
https://visibility.buzzintel.co/tracker/clients/460de648-ddd0-4cf3-bee6-a15bc28c1bd4

**Focus only on the "SEO Work & Stats" tab** on that page. Do not work on the other tabs
(Client, Onboarding, Monthly Strategy, Social) or other task categories (Technical, Off Page,
GMB, AI, Admin) unless explicitly asked.

## Scope within SEO Work & Stats
- On Page **technical fixes only**: missing H1, missing page title, missing meta description,
  missing OG/Twitter tags, thin content on individual pages.
- Explicitly excluded (user's choice): broad content-creation tasks — publishing a blog/insights
  hub, writing full in-depth service pages, building location pages, or drafting FAQ answers.
  Do not write new site content without being asked again.
- **Skip `/info/` (WP page id 485) entirely.** It's a password-protected page showing the firm's
  bank transfer details (sort code/account number) for client conveyancing payments — deliberately
  obscure to reduce payment-diversion fraud risk. Do not add titles/H1/meta description/OG tags to
  it; that would make it more discoverable, which is the opposite of the intent.

## Reliability notes
- The Legalbuzz dashboard's task board (Done/To-do counts, "Verified on site" labels) has been
  observed to be unreliable: it flips task status and changes affected-page counts without any
  corresponding edit actually happening on the live WordPress site. Always cross-check against the
  live site directly (WordPress REST API) before trusting a "Done"/"Verified" claim there.
- jpgoldman.co.uk is hosted behind SiteGround's bot-protection (SG Security), which escalates to a
  CAPTCHA challenge under rapid/automated requests. Pace requests when scripting against it; avoid
  parallel or rapid-fire retries.

## Access
- Legalbuzz dashboard login and the WordPress application password were provided directly in
  chat, not stored in this repo — ask the user again if a new session needs them.
- WPVibe (AI-native WordPress management plugin, via `mcp.wpvibe.ai`) is installed on the site and
  is the preferred path for future WordPress edits once connected, in place of raw REST API
  scripting through a headless browser.

## Reporting format (user preference — always use this)

**Single finding** (one item, e.g. "is item X real, what's its status"): lead with a scannable
header block before any supporting detail, so the user can read the verdict immediately without
hunting for it in prose:

```
STATUS: ✅ Confirmed / ❌ Not real / ⚠️ Needs check / 🔧 Fixed
ITEM: what this is about
FINDING: one-line verdict
DETAILS: supporting specifics (only as long as needed)
NEXT: what happens next, or what's needed from the user
```

**Multiple items** (e.g. a task list, several findings in one report): give each item its own
separated box, mirroring how the Legalbuzz CRM shows one card per task — do not merge them into a
single paragraph or a combined table. One box per item, in this shape:

```
**TASK N — <task name>**
- Status: <To do/Done/etc> · Urgency: <High/Medium/Low>
- Found by site check: <the claim/count and what page(s) it names>
- Reality check: <what's actually true on the live site, if verified>
---
```

Separate each box with a horizontal rule (`---`). After all the boxes, add a short "Bottom line"
line if there's a common thread across items, and a NEXT line if there's an open question or
action needed.

In both cases: keep DETAILS/bullets terse — bullet points over paragraphs. Only include a NEXT
line when there's an actual next step or open question.
