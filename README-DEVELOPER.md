# Developer Guide

Detailed architecture and conventions for contributing to the Websitepolierer codebase.

## Architecture Overview

This is a zero-dependency static website. There are no build steps, no bundlers, no package managers. The `website/` directory IS the deployment artifact.

### Sales Funnel Structure

`index.html` is a single-page layout following a conversion funnel:

| Section | ID | Purpose |
|---------|-----|---------|
| Hero | `#hero` | Attention — 48h promise, CTAs, stats |
| Social Proof | — | Trust — 3 testimonials with star ratings |
| Leistungen | `#leistungen` | Value — 4 service cards |
| Branchen | `#branchen` | Relevance — 5 industry cards with demo links |
| Process | `#ablauf` | Simplicity — 3-step timeline |
| Pricing | `#preise` | Price anchoring — 3 tiers |
| Compare | — | Objection handling — table vs. Baukasten |
| FAQ | `#faq` | Objection handling — 9 accordion items |
| About | `#ueber` | Personal — owner photo, trust badges |
| Contact | `#kontakt` | Action — form + email link |
| Footer | — | Navigation, legal links, demo links |
| Sticky CTA | — | Mobile-only bottom bar (after 400px scroll) |

## CSS Architecture

### Custom Properties (`:root`)

```css
/* Colors */
--accent: #1a56db          /* Primary blue */
--accent-hover: #1348b8    /* Button hover */
--accent-light: #e8eefb    /* Light blue backgrounds */
--bg-white: #ffffff         /* Page background */
--bg-light: #f7f7f8        /* Alternating section bg */
--text-dark: #1a1a1a       /* Headings */
--text-body: #3d3d3d       /* Body text */
--text-muted: #6b6b6b      /* Secondary text */
--text-light: #999999      /* Tertiary text */
--border: #e5e5e5          /* Card/element borders */
--border-hover: #d0d0d0    /* Border hover state */

/* Layout */
--radius: 8px              /* Standard border-radius */
--radius-lg: 12px          /* Large border-radius (cards) */
--font: 'Inter', -apple-system, ...  /* Font stack */
--transition: 0.2s ease    /* Standard transition */
```

### BEM Naming Convention

```
.block                     (e.g., .nav, .pricing, .hero)
.block__element            (e.g., .nav__link, .pricing__card)
.block__element--modifier  (e.g., .nav__burger--active, .pricing__card--featured)
```

Exceptions: utility classes like `.container`, `.anim-fade-up`, `.text-accent`, `.section-tag`, `.section-title`.

### Section CSS Pattern

Each major section follows:
```css
/* ======== SECTION NAME ======== */
.section-name { padding: 100px 0; }
.section-name__grid { display: grid; ... }
.section-name__card { ... }
```

### Responsive Breakpoints

| Breakpoint | Target | Key Changes |
|-----------|--------|-------------|
| 1024px | Tablet | Pricing single-column, about stacked, footer 2-col |
| 768px | Mobile | Burger menu activates, single-column grids, sticky CTA appears, footer 80px bottom padding |
| 480px | Small | Hero CTAs stack vertically |

All responsive rules are at the bottom of `style.css` in `@media` blocks.

### Animation System

1. Add class `anim-fade-up` to any element
2. JavaScript IntersectionObserver adds `anim-visible` when element enters viewport
3. Use `data-delay="100"` attribute for staggered timing (milliseconds)
4. CSS handles the transition: `opacity 0→1`, `translateY 30px→0`

## JavaScript Patterns

### Scroll Behavior
- Nav adds `.nav--scrolled` after 60px scroll (adds shadow + solid bg)
- Sticky CTA adds `.sticky-cta--visible` after 400px scroll (mobile only)

### Mobile Menu
- Burger toggle: `.nav__burger--active` + `.nav__links--open` + `body.no-scroll`
- Auto-closes on any link click inside nav

### Smooth Scroll
- All `a[href^="#"]` links get smooth scroll with offset for fixed nav height

### Contact Form
- **NO backend** — `action="#"` with JavaScript handler
- On submit: shows checkmark SVG + "Nachricht gesendet!" for 3 seconds, then resets
- **TODO:** Needs actual backend integration (Formspree, Netlify Forms, or custom API)

## How to Add/Modify Content

### New FAQ Item
Insert inside `.faq__list`:
```html
<details class="faq__item anim-fade-up" data-delay="XXX">
  <summary class="faq__question">Question?</summary>
  <div class="faq__answer"><p>Answer.</p></div>
</details>
```

### New Demo Page
1. Copy an existing demo from `website/demos/` as a template
2. Update CSS custom properties at the top for new color scheme
3. Set `<meta name="robots" content="noindex, nofollow">`
4. Reference fonts as `../assets/fonts/inter-latin.woff2`
5. Add a link card in the Branchen section of `index.html`
6. Add a link in the footer demos column

### New Section in index.html
1. Follow the section pattern: `section > .container > .section-header > .grid`
2. Add CSS in `style.css` with a `/* ======== NAME ======== */` comment block
3. If it needs a nav anchor, add the ID and a `<a>` in the nav
4. Add `anim-fade-up` classes for scroll animations
5. Add responsive styles in the existing `@media` blocks

### New Pricing Feature
Add an `<li>` inside `.pricing__features`:
```html
<li>
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
    <path d="M4 9l3.5 3.5L14 5" stroke="#1a56db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  Feature description
</li>
```

## SEO

- Title: include primary keyword + location (Berlin)
- Meta description: under 160 chars, include value proposition
- Schema.org JSON-LD: `ProfessionalService` type in `<head>`
- OpenGraph tags: `og:title`, `og:description`, `og:type`, `og:url`
- Only ONE `<h1>` per page
- Heading hierarchy: h1 → h2 → h3, no skips
- All images must have `alt` attributes
- Demo pages are `noindex, nofollow`

## GDPR / Legal Compliance

| Rule | Reason |
|------|--------|
| Self-hosted fonts | No Google Fonts CDN calls (DSGVO) |
| No external analytics | No tracking without Datenschutz update |
| No cookies set | No cookie banner required |
| Impressum required | German law (TMG SS 5) |
| Datenschutz required | GDPR Article 13 |

**Never add** Google Analytics, Facebook Pixel, Hotjar, or similar without updating the Datenschutz page and discussing with the owner.

## Git Workflow

- Single branch: `master`
- Commits use conventional format: `feat:`, `fix:`, `docs:`, `refactor:`
- Push to master triggers auto-deploy to Vercel
- Always test locally at 4 breakpoints before pushing
- No CI/CD pipeline — Vercel handles deployment directly

## Performance Budget

| Metric | Current | Limit |
|--------|---------|-------|
| CSS size | ~30KB | 35KB |
| JS size | ~3KB | 10KB |
| External requests | 0 | 0 |
| Font files | 2 (WOFF2) | 2 |
| Images | 2 (logo + photo) | Keep minimal |
