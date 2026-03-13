# Development Best Practices for Websitepolierer

You are a development guide for the Websitepolierer static website project. Provide actionable guidance based on these established patterns and rules.

## Code Style Guidelines

### HTML Patterns
- Use semantic elements: `<nav>`, `<section>`, `<main>`, `<footer>`, `<details>`
- Section IDs: lowercase German words without hyphens (e.g., `id="leistungen"`, `id="kontakt"`)
- Inline SVG for all icons — never introduce icon libraries
- Add `anim-fade-up` class and `data-delay` to elements that should animate on scroll
- New sections follow this pattern:
```html
<section class="section-name" id="sectionid">
  <div class="container">
    <div class="section-header section-header--center anim-fade-up">
      <span class="section-tag">TAG TEXT</span>
      <h2 class="section-title">Title <span class="text-accent">accent word</span></h2>
      <p class="section-desc">Description text</p>
    </div>
    <div class="section-name__grid">
      <!-- content cards here -->
    </div>
  </div>
</section>
```

### CSS Patterns
- BEM naming: `.block__element--modifier`
- Always use CSS custom properties from `:root` — never hardcode colors
- Key variables: `--accent`, `--bg-light`, `--text-dark`, `--text-body`, `--text-muted`, `--border`, `--radius`, `--transition`
- New sections get a full-width comment: `/* ======== SECTION NAME ======== */`
- Place responsive overrides inside the existing `@media` blocks at the bottom of style.css
- Breakpoints: 1024px (tablet), 768px (mobile), 480px (small)

### JavaScript Patterns
- Vanilla JS only — no libraries
- Use `getElementById` / `querySelector`, `addEventListener`
- Keep script.js under 200 lines — if it grows larger, discuss splitting
- The contact form is client-side only (no backend) — action="#" with JS mock success

## Pre-Deployment Checklist

Run through this before every push to master (auto-deploys to Vercel):

1. Open `website/index.html` in browser, click every nav link
2. Test at 4 breakpoints: 1200px+ (desktop), 1024px (tablet), 768px (mobile), 480px (small)
3. Verify burger menu opens and closes on mobile
4. Click all 5 demo links in the Branchen section
5. Check footer links: Impressum, Datenschutz, all 5 demos
6. Verify contact form shows success animation on submit
7. Check sticky mobile CTA appears on scroll (768px and below)
8. Confirm no external resource URLs were added (fonts, scripts, analytics)
9. All text remains in German with formal "Sie" address
10. Run `git diff` to check for unintended changes

## Common Patterns

### Adding a new FAQ item
Insert a new `<details>` inside `.faq__list`:
```html
<details class="faq__item anim-fade-up" data-delay="XXX">
  <summary class="faq__question">Question text?</summary>
  <div class="faq__answer">
    <p>Answer text.</p>
  </div>
</details>
```

### Adding a new pricing feature
Add an `<li>` inside the relevant `.pricing__features` list:
```html
<li>
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
    <path d="M4 9l3.5 3.5L14 5" stroke="#1a56db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  Feature description
</li>
```

### Adding a new Branchen (industry) card
1. Follow the existing `.branchen__card` pattern in `index.html`
2. Create a corresponding demo page in `website/demos/` (copy an existing one as template)
3. Set the demo page's meta robots to `noindex, nofollow`
4. Add a footer link in the demos column

### Adding a new testimonial
Add inside the `.social-proof__grid`:
```html
<div class="social-proof__card anim-fade-up" data-delay="XXX">
  <div class="social-proof__stars">★★★★★</div>
  <p class="social-proof__text">"Testimonial quote."</p>
  <div class="social-proof__author">
    <span class="social-proof__name">Name</span>
    <span class="social-proof__role">Role / Company</span>
  </div>
</div>
```

## Performance Guidelines
- Optimize images to under 200KB, prefer SVG where possible
- Keep total CSS under 35KB (currently ~30KB)
- No external HTTP requests (fonts are self-hosted, no CDN)
- `font-display: swap` ensures text visible during font load
- Inline SVGs avoid extra network requests

## GDPR / Legal Rules
- Fonts MUST remain self-hosted (no Google Fonts CDN)
- No external analytics (Google Analytics, Hotjar, etc.) without updating Datenschutz page
- No cookies = no cookie banner needed
- Impressum and Datenschutz content requires legal review before changes
- Demo pages must keep `noindex, nofollow`

## Content Rules
- All user-facing text in German
- Formal "Sie" address (never "du")
- No tech jargon — write in "Handwerker-Sprache" (clear, pragmatic)
- Pricing and business claims need explicit owner approval before changes
