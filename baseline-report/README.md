# SEO Baseline Report

Builds the onboarding baseline PDF (site health, keyword rankings, backlink profile) for a client, ready to attach to the CRM.

## New client
1. Copy `data/_template.json` to `data/<client>.json` and fill it in.
   - Site health: run Lighthouse / PageSpeed Insights on the homepage (mobile and desktop).
   - Rankings: `location` = keywords with a place name, `service` = practice-area keywords. Leave `position` null when not ranking.
   - Backlinks: figures from the Legalbuzz dashboard.
   - Leave anything unknown as `null` — it prints as "—" and empty sections show an "Awaiting data" note. Never guess numbers.
2. Build: `NODE_PATH=/opt/node-tools/node_modules node build.js data/<client>.json`
3. PDF lands in `output/<client>-seo-baseline.pdf`.

Needs Node with Playwright (Chromium) and `pdfunite` (poppler-utils).
