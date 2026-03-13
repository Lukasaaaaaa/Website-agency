# Websitepolierer — Agency Website

## Project Overview
- **What:** Landing page for a Berlin-based web agency targeting KMUs (small businesses)
- **Live URL:** https://websitepolierer.de
- **Owner:** Lukas Gurny, Berlin
- **Target clients:** Handwerker (tradespeople), Praxen (medical practices), Gartenbau (landscaping), Notdienste (emergency services), Dienstleister (service providers)
- **Business model:** Custom websites from EUR 1,500 one-time + EUR 79/mo maintenance, EUR 299 SEO package
- **Key promise:** Draft in 48 hours, "erst schauen, dann zahlen" (see before you pay)

## Tech Stack
- Pure vanilla HTML5 / CSS3 / JavaScript — NO frameworks, NO Node.js, NO build tools
- No package.json, no dependencies to install
- Deployment: Vercel static hosting, auto-deploys from GitHub master branch
- Vercel root directory: `website/`
- Git remote: https://github.com/Lukasaaaaaa/Website-agency.git (master branch)

## File Structure
```
website/
  index.html             Main landing page (single-page with anchor sections)
  style.css              All styles (BEM naming, CSS custom properties)
  script.js              Vanilla JS (nav, animations, form handler)
  impressum.html         Legal: Impressum (noindex)
  datenschutz.html       Legal: Datenschutzerklaerung (noindex)
  RESEARCH-AGENCY-WEBSITE.md   59KB research document (German)
  assets/
    logo.svg             SVG logo
    inhaber.jpg          Owner photo (About section)
    fonts/
      inter-latin.woff2        Self-hosted Inter font (GDPR-compliant)
      inter-latin-ext.woff2    Inter Latin Extended subset
  demos/
    handwerker.html      Electrician demo (self-contained, inline CSS/JS)
    gartenbau.html       Landscaping demo
    praxis.html          Medical practice demo
    notdienst.html       Emergency service demo
    dienstleister.html   B2B service provider demo
```

## Page Sections (index.html, in order)
1. **Navigation** — fixed, scrolled state after 60px, mobile burger menu
2. **Hero** (#hero) — badge "In 48h fertig", title, subtitle, 2 CTAs, 3 stats
3. **Social Proof** — 3 testimonial cards with 5-star ratings
4. **Leistungen** (#leistungen) — 4 service cards (Webdesign, Mobile, SEO, Google My Business)
5. **Branchen** (#branchen) — 5 industry cards with mockup visuals + demo links
6. **Process** (#ablauf) — 3-step timeline
7. **Pricing** (#preise) — 3 pricing cards (EUR 1,500 / EUR 79/mo / EUR 299)
8. **Compare** — Table comparing Baukasten vs. Websitepolierer
9. **FAQ** (#faq) — 9 accordion items using `<details>`/`<summary>`
10. **About** (#ueber) — Personal section with photo, trust badges
11. **Contact** (#kontakt) — Form (NO backend) + email link
12. **Footer** — Nav links, demo links, legal links
13. **Sticky Mobile CTA** — Fixed bottom bar (mobile only, appears after 400px scroll)

## Coding Conventions

### CSS
- **BEM naming:** `.block__element--modifier` (e.g., `.nav__link`, `.pricing__card--featured`)
- **CSS custom properties** in `:root` for all colors, radii, fonts, transitions:
  - `--accent: #1a56db`, `--accent-hover: #1348b8`, `--accent-light: #e8eefb`
  - `--bg-white: #ffffff`, `--bg-light: #f7f7f8`
  - `--text-dark: #1a1a1a`, `--text-body: #3d3d3d`, `--text-muted: #6b6b6b`
  - `--border: #e5e5e5`, `--radius: 8px`, `--radius-lg: 12px`
  - `--font: 'Inter', -apple-system, ...`, `--transition: 0.2s ease`
- **Section comments:** `/* ======== SECTION NAME ======== */`
- **Responsive breakpoints:** 1024px (tablet), 768px (mobile), 480px (small mobile)
- **Animations:** `.anim-fade-up` class + `.anim-visible` toggled by IntersectionObserver, `data-delay` for staggered timing

### HTML
- Semantic HTML5: `<nav>`, `<section>`, `<main>`, `<footer>`, `<details>`/`<summary>`
- All SVG icons are inline (no icon library)
- Section IDs for anchor navigation: `#hero`, `#leistungen`, `#branchen`, `#ablauf`, `#preise`, `#faq`, `#ueber`, `#kontakt`

### JavaScript
- Vanilla JS only, no libraries
- Features: sticky nav, burger menu, smooth scroll, IntersectionObserver animations, sticky mobile CTA, form submit handler
- **The contact form has NO backend** — it shows a success animation then resets after 3 seconds

### Content
- ALL user-facing text is in German
- Formal address ("Sie" not "du")
- Tone: pragmatic, clear, no tech jargon
- SEO: German meta descriptions, keywords, Schema.org JSON-LD (ProfessionalService), OpenGraph tags

### Demo Pages
- Each demo is SELF-CONTAINED (inline `<style>` + inline `<script>`)
- They reference `../assets/fonts/` for Inter font
- All marked `noindex, nofollow`
- Each has its own color scheme via CSS custom properties

## Design Decisions (Do NOT Change Without Discussion)
- NO frameworks (React, Vue, etc.) — deliberate choice for simplicity and speed
- NO Google Fonts CDN — self-hosted Inter for DSGVO/GDPR compliance
- NO external analytics or tracking scripts
- NO cookie banner needed (no cookies are set)
- Fonts use `font-display: swap` for performance

## Deployment
- Push to `master` branch → Vercel auto-deploys from `website/` directory
- Domain: websitepolierer.de
- No build step needed

## How to Run Locally
```bash
cd website && python3 -m http.server 8000
# Visit http://localhost:8000
```
Or simply open `website/index.html` directly in a browser.

## Safety Rules
- NEVER add external scripts (Google Fonts, analytics, tracking) without discussing GDPR implications
- NEVER change pricing, business claims, or contact information without explicit approval
- NEVER modify the Impressum or Datenschutz content without legal review
- NEVER remove `noindex` from demo pages
- Keep all SVG icons inline — do not switch to an icon library
- Test all changes at 1024px, 768px, and 480px widths
- The contact form has no backend — any backend integration needs separate discussion

## Before Committing
1. Visually verify changes at desktop (1200px+), tablet (1024px), mobile (768px), small (480px)
2. Check that all anchor links (#leistungen, #branchen, etc.) still work
3. Verify demo page links in the Branchen section still open correctly
4. Ensure no external resources were inadvertently added
5. Run `/qa` skill to verify the live site matches expectations

## Available Skills
- `/dev-guide` — Development best practices and coding patterns for this codebase
- `/qa` — Full QA check of the live site using WebFetch (pages, links, SEO, assets, local vs live comparison)
