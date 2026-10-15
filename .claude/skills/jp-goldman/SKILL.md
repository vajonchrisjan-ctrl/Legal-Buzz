---
name: jp-goldman
description: Client brief for JP Goldman (jpgoldman.co.uk) SEO work in the Legalbuzz dashboard — scope, exclusions, site access and reliability notes. Use only when the session is about JP Goldman (the user names JP Goldman or jpgoldman.co.uk, or runs /jp-goldman). Do not apply to other clients or general SEO questions.
---

# JP Goldman — SEO Work scope

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

## Site notes
- jpgoldman.co.uk is hosted behind SiteGround's bot-protection (SG Security), which escalates to a
  CAPTCHA challenge under rapid/automated requests. Pace requests when scripting against it; avoid
  parallel or rapid-fire retries.
- Always cross-check Legalbuzz board claims against the live site directly (WordPress REST API)
  before trusting a "Done"/"Verified" status.

## Access
- The WordPress application password was provided directly in chat, not stored in this repo — ask
  the user again if a new session needs it.
- WPVibe (AI-native WordPress management plugin, via `mcp.wpvibe.ai`) is installed on the site and
  is the preferred path for WordPress edits once connected, in place of raw REST API scripting
  through a headless browser.

## Reporting
In the LIVE SITE CHANGE line of the reporting format (see root CLAUDE.md), the live site is
jpgoldman.co.uk.
