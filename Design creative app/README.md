# Design creative app
Prompt an idea → the Research, Writing and Design agents produce Ads, Proposal and Post creative, previewed in a dashboard.

    agents/research.js   Research Agent  (audience, pains, angle)
    agents/writing.js    Writing Agent   (ads / proposal / post copy)
    agents/design.js     Design Agent    (palette, type, layout, art direction)
    agents/llm.js        shared Claude API caller
    agents/demo.js       offline stand-ins when no API key is set
    server.js            pipeline + web server
    public/              dashboard UI
    docs/                static demo for GitHub Pages
    claude-artifact/     source of the claude.ai-hosted version

Run locally (Node 18+, no dependencies):

    ANTHROPIC_API_KEY=sk-... node server.js   # live agents (optional CLAUDE_MODEL)
    node server.js                            # demo mode
    open http://localhost:3000
