# Websitepolierer

Professional websites for tradespeople and local businesses in Berlin.

**Live:** https://websitepolierer.de

## What Is This?

Landing page for Websitepolierer, a Berlin-based web agency that builds websites for small businesses (KMUs) — electricians, plumbers, medical practices, landscapers, and other local service providers.

The site includes:
- A conversion-optimized landing page with social proof, pricing, FAQ, and contact form
- 5 industry-specific demo websites (Handwerker, Gartenbau, Praxis, Notdienst, Dienstleister)
- Legal pages (Impressum, Datenschutzerklarung)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Markup | HTML5 (semantic, Schema.org structured data) |
| Styling | CSS3 (custom properties, BEM naming, responsive) |
| Scripting | Vanilla JavaScript (no libraries) |
| Fonts | Inter (self-hosted WOFF2, GDPR-compliant) |
| Hosting | Vercel (static, auto-deploy from GitHub) |
| Domain | websitepolierer.de |

No build tools, no Node.js, no package.json. Just files and a browser.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Lukasaaaaaa/Website-agency.git
cd Website-agency

# Serve locally
cd website
python3 -m http.server 8000
# Visit http://localhost:8000
```

Or simply open `website/index.html` in your browser.

## Project Structure

```
website/
  index.html              Main landing page
  style.css               All styles
  script.js               JavaScript (nav, animations, form)
  impressum.html           Legal: Impressum
  datenschutz.html         Legal: Privacy policy
  assets/
    logo.svg              Company logo
    inhaber.jpg           Owner photo
    fonts/                Self-hosted Inter (WOFF2)
  demos/
    handwerker.html       Electrician demo
    gartenbau.html        Landscaping demo
    praxis.html           Medical practice demo
    notdienst.html        Emergency service demo
    dienstleister.html    Service provider demo
```

## Deployment

The site auto-deploys to Vercel when changes are pushed to the `master` branch. Vercel serves the `website/` directory as the root. No build step is needed.

## Documentation

- [README-DEVELOPER.md](README-DEVELOPER.md) — Coding conventions, architecture, and how to make changes
- [README-USER.md](README-USER.md) — End-user guide for navigating the website and services
- [CLAUDE.md](CLAUDE.md) — Claude Code agent configuration (full project context)

## Claude Code Integration

This project is configured for Claude Code with:
- `CLAUDE.md` — Full project context and safety rules
- `.claude/commands/dev-guide.md` — `/dev-guide` skill for coding best practices
- `.claude/commands/qa.md` — `/qa` skill for live site quality assurance

## License

All rights reserved. Copyright 2026 Websitepolierer / Lukas Gurny.
