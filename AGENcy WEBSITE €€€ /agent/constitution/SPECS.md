# SPECS.md - Website Generation Constitution

## MANDATORY: Read this file COMPLETELY before EVERY website generation.

## 1. Tech Stack (non-negotiable)
- Output: Single-file static HTML. Everything in ONE file.
- Styling: Tailwind CSS via CDN
- Fonts: system-ui stack ONLY. NO Google Fonts CDN (DSGVO violation).
- JS: Vanilla only. Mobile menu toggle + smooth scroll. Nothing else.
- NO external dependencies except Tailwind CDN.

### Required <head> block (copy exactly):
```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex, nofollow">
    <meta name="description" content="[FIRMENNAME] - [KERNLEISTUNG] in [STADT]. [1 Satz USP]">
    <title>[FIRMENNAME] - [KERNLEISTUNG] in [STADT]</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        accent: '[ACCENT_HEX]',
                        dark: '#0a0a0a',
                    }
                }
            }
        }
    </script>
    <style>
        * { font-family: 'Inter', system-ui, -apple-system, sans-serif; }
        html { scroll-behavior: smooth; }
        .glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); }
        .glow { box-shadow: 0 0 40px rgba(var(--accent-rgb), 0.12); }
        .glow-sm { box-shadow: 0 0 20px rgba(var(--accent-rgb), 0.08); }
        @keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .fade-up { animation: fadeUp 0.6s ease-out forwards; }
        .fade-up-delay-1 { animation-delay: 0.1s; opacity: 0; }
        .fade-up-delay-2 { animation-delay: 0.2s; opacity: 0; }
        .fade-up-delay-3 { animation-delay: 0.3s; opacity: 0; }
    </style>
</head>
```

## 2. Visual Identity ("Accessible Premium")

The goal: Look like a 5.000 EUR agency website, but built for a 55-year-old
Handwerksmeister. Premium but approachable. Dark but warm. Modern but readable.

### Color System
| Token | Value | Usage |
|-------|-------|-------|
| Background | #0a0a0a | <body> and all major sections |
| Surface | rgba(255,255,255,0.05) | Cards, navbar, containers (use .glass class) |
| Surface Hover | rgba(255,255,255,0.08) | Card hover state |
| Primary Text | #f5f5f5 | Headlines, important text |
| Secondary Text | #a3a3a3 | Body text, descriptions |
| Muted Text | #525252 | Labels, timestamps, captions |
| Accent | varies by niche | CTA buttons, highlights, icons, glow |
| Accent Low | accent at 10% opacity | Badge backgrounds, subtle highlights |
| Border | rgba(255,255,255,0.08) | Card borders, dividers |
| Success | #22c55e | WhatsApp buttons, positive indicators |

### Typography Scale
- Hero headline: text-4xl md:text-6xl font-bold tracking-tight
- Section headings: text-3xl md:text-4xl font-bold
- Subheadings: text-xl md:text-2xl font-semibold
- Body large: text-lg text-neutral-400 leading-relaxed
- Body: text-base text-neutral-400
- Small/Caption: text-sm text-neutral-500

### Component Patterns

#### Glassmorphism Card (use everywhere):
```html
<div class="glass rounded-2xl p-6 md:p-8 hover:bg-white/[0.08] transition-all duration-300">
    <!-- content -->
</div>
```

#### CTA Button (primary):
```html
<a href="#" class="inline-flex items-center gap-2 bg-accent hover:bg-accent/90 text-white font-semibold px-8 py-4 rounded-full transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-accent/20">
    Button Text
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
</a>
```

#### CTA Button (secondary/outline):
```html
<a href="#" class="inline-flex items-center gap-2 border border-white/20 hover:border-accent/50 text-white font-medium px-8 py-4 rounded-full transition-all duration-300 hover:bg-white/5">
    Button Text
</a>
```

#### Section Container Pattern:
```html
<section id="section-id" class="py-20 md:py-32">
    <div class="max-w-6xl mx-auto px-6">
        <div class="text-center mb-16">
            <span class="text-accent text-sm font-semibold tracking-widest uppercase">Section Label</span>
            <h2 class="text-3xl md:text-4xl font-bold text-white mt-4">Section Heading</h2>
            <p class="text-lg text-neutral-400 mt-4 max-w-2xl mx-auto">One sentence description.</p>
        </div>
        <!-- Section content -->
    </div>
</section>
```

#### Star Rating Badge:
```html
<div class="inline-flex items-center gap-2 glass rounded-full px-4 py-2">
    <div class="flex text-yellow-400">
        <!-- Repeat star SVG for each full star -->
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
    </div>
    <span class="text-white font-semibold">[STERNE]</span>
    <span class="text-neutral-400 text-sm">([BEWERTUNGEN] Google Bewertungen)</span>
</div>
```

#### Image Placeholder (NOT a gray box - use gradient):
```html
<div class="aspect-video rounded-2xl bg-gradient-to-br from-accent/20 via-accent/5 to-transparent flex items-center justify-center border border-white/5">
    <div class="text-center">
        <svg class="w-12 h-12 text-accent/40 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
        <span class="text-sm text-neutral-500">[BESCHREIBUNG]</span>
    </div>
</div>
```

### FORBIDDEN
- Gray boxes (#333 divs) as image placeholders
- Lorem ipsum or any Latin filler text
- Stock photo URLs (use placeholder gradients)
- WebGL, Three.js, heavy JS animations
- Parallax scrolling
- More than 2 font weights (semibold + bold only, plus normal for body)
- Inline styles (use Tailwind classes, except for the <style> block above)
- Comic Sans, Papyrus, or decorative fonts

## 3. Mandatory Page Structure (EVERY site)

### Navigation (sticky):
```html
<nav class="fixed top-0 w-full z-50 glass">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <a href="#" class="text-xl font-bold text-white">[FIRMENNAME]</a>
        <!-- Desktop links -->
        <div class="hidden md:flex items-center gap-8">
            <a href="#leistungen" class="text-neutral-400 hover:text-white transition">Leistungen</a>
            <a href="#ueber-uns" class="text-neutral-400 hover:text-white transition">Ueber uns</a>
            <a href="#bewertungen" class="text-neutral-400 hover:text-white transition">Bewertungen</a>
            <a href="#kontakt" class="bg-accent hover:bg-accent/90 text-white px-6 py-2.5 rounded-full font-medium transition-all hover:scale-105">[SHORT_CTA]</a>
        </div>
        <!-- Mobile hamburger -->
        <button id="menu-toggle" class="md:hidden text-white">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
    </div>
    <!-- Mobile menu (hidden by default) -->
    <div id="mobile-menu" class="hidden md:hidden px-6 pb-6 space-y-4">
        <a href="#leistungen" class="block text-neutral-300 hover:text-white py-2">Leistungen</a>
        <a href="#ueber-uns" class="block text-neutral-300 hover:text-white py-2">Ueber uns</a>
        <a href="#bewertungen" class="block text-neutral-300 hover:text-white py-2">Bewertungen</a>
        <a href="#kontakt" class="block bg-accent text-white text-center px-6 py-3 rounded-full font-medium">[SHORT_CTA]</a>
    </div>
</nav>
```

### Section 1: Hero
- Full viewport height on mobile (min-h-screen), generous padding on desktop
- Company name as h1 (text-4xl md:text-6xl font-bold)
- Tagline as p (text-lg md:text-xl text-neutral-400, max 2 lines)
- Primary CTA button (large, accent color, with arrow icon)
- Secondary CTA button (outline, e.g. "Mehr erfahren" or phone number)
- Star rating badge below CTAs
- Subtle radial gradient glow behind hero content

### Section 2: Services/Leistungen
- Section label + heading + description (use Section Container Pattern)
- Grid: grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6
- Each service as .glass card with:
  - SVG icon (accent colored, w-10 h-10, simple line-art style)
  - Service name (text-xl font-semibold text-white)
  - 2-sentence description (text-neutral-400)
- Use REAL service names for the niche, not generic placeholders

### Section 3: About / Ueber uns
- Two-column layout on desktop (content left, image placeholder right)
- Short compelling text about the company (3-4 sentences, written for the niche)
- Key stats in a row: "XX+ Jahre Erfahrung", "XXX+ Projekte", "X.X★ Google"
- Image placeholder using gradient pattern (NOT a gray box)

### Section 4: Social Proof / Bewertungen
- Star rating badge (prominent, centered)
- 2-3 testimonial cards in a grid
- Each testimonial: quote text, author name, role/context
- Use realistic German names and plausible review content for the niche
- Do NOT use real names from the lead data for testimonials (fake reviews are illegal)

### Section 5: CTA Repeat
- Full-width section with accent gradient background (subtle, not overwhelming)
- Headline restating the value proposition
- CTA button (same as hero)
- Optional: phone number with tel: link

### Section 6: Footer
- Glass background
- Company name, address placeholder [ADRESSE], phone, email placeholder
- Navigation links (same as header)
- **MANDATORY:** "Impressum" link and "Datenschutzerklaerung" link
- Copyright line with current year
- Minimal, no clutter

### Mobile Menu JS (place before </body>):
```html
<script>
    const toggle = document.getElementById('menu-toggle');
    const menu = document.getElementById('mobile-menu');
    toggle.addEventListener('click', () => menu.classList.toggle('hidden'));
    document.querySelectorAll('#mobile-menu a').forEach(a =>
        a.addEventListener('click', () => menu.classList.add('hidden'))
    );
</script>
```

## 4. Industry Routing

### Handwerker (Elektriker, Maler, Dachdecker, SHK)
- Archetype: Recruiting Funnel
- Goal: Employee recruitment (NOT customer acquisition)
- Accent: #06b6d4 (cyan) | --accent-rgb: 6,182,212
- Hero CTA: "Bewerbung in 60 Sekunden" (green WhatsApp button: bg-green-500)
- Hero secondary: "Unsere Leistungen" (outline button)
- Extra section BEFORE services: "Warum bei uns arbeiten?"
  - Benefits cards: 4-Tage-Woche, Firmenwagen, Ueberdurchschnittliches Gehalt, Weiterbildung, Modernes Werkzeug
  - Each benefit as glass card with icon + title + 1-sentence description
- Testimonials: From EMPLOYEES, not customers ("Seit 3 Jahren im Team...")
- Tone: Direct, Kumpel-Ton. "Bock auf ein starkes Team?" not "Werden Sie Teil unseres Teams."
- Icons: wrench, lightning bolt, hard hat, tools

### Physiotherapie / Praxis
- Archetype: Booking Bridge
- Goal: Private patients / self-payers
- Accent: #14b8a6 (teal) | --accent-rgb: 20,184,166
- Hero CTA: "Termin online buchen" (links to #booking)
- Extra section: Team profiles
  - 2-3 therapist cards with photo placeholder, name, qualification, specialization
  - Use realistic titles: "M.Sc. Physiotherapie", "Osteopath D.O.", "Heilpraktiker Physiotherapie"
- Services focus: "Leistungen fuer Selbstzahler" - Osteopathie, Manuelle Therapie, Sportphysiotherapie, Lymphdrainage
- Testimonials: From PATIENTS ("Nach 3 Sitzungen schmerzfrei...")
- Tone: Calm, empathetic, medically competent. Use "Sie" form throughout.
- Icons: heart, spine, hand, person-running

### GaLaBau (Garten- und Landschaftsbau)
- Archetype: Before/After Showcase
- Goal: High-ticket projects (50k+ EUR)
- Accent: #22c55e (green) | --accent-rgb: 34,197,94
- Hero CTA: "Kostenloses Erstgespraech fuer Ihr Projekt"
- Extra section: Project Showcase (THE visual centerpiece)
  - 2x3 grid of project cards
  - Each card: category label, large image placeholder, "Vorher" / "Nachher" split
  - Categories: Poolbau, Terrassengestaltung, Gartenplanung, Bepflanzung, Beleuchtung, Naturstein
- Minimal text overall. Let images sell.
- Testimonials: From HOMEOWNERS ("Unser Garten ist jetzt unser Lieblingsort...")
- Tone: Aspirational, luxury. "Ihr Traumgarten" not "Wir machen Gaerten."
- Icons: tree, water drop, sun, ruler

### Fahrschule
- Archetype: Direct Response
- Goal: Student signups
- Accent: #8b5cf6 (violet) | --accent-rgb: 139,92,246
- Hero CTA: "Jetzt anmelden" (prominent, sticky on mobile via fixed bottom bar)
- Extra section: Price table
  - Glass table with: Grundgebuehr, Fahrstunde (45 Min), Sonderfahrten, Theorie-Kurs
  - Use [PREIS] placeholders for all amounts
- Extra section: "Naechste Theorie-Kurse" with date placeholders
- Testimonials: From STUDENTS ("Beim ersten Versuch bestanden!")
- Tone: Casual, young, encouraging. "Du" form.
- Icons: car, license, calendar, thumbs-up

### Schluesseldienst / Notdienst
- Archetype: Emergency Site
- Goal: Immediate phone calls
- Accent: #ef4444 (red) | --accent-rgb: 239,68,68
- Hero CTA: MASSIVE "Jetzt anrufen" button with tel: link
  - Must be visible without scrolling on mobile
  - Add sticky bottom bar on mobile with phone button
- FEWER sections (speed is everything): Hero, Services, Service Area, Footer
- No testimonials section (nobody reads reviews in an emergency)
- Service area: List of Stadtteile/PLZ served
- "24/7 Notdienst" badge in header
- Tone: Reassuring, immediate, no-nonsense.
- MINIMAL animations (fast page load is critical)

### Gebaeudereinigung / B2B
- Archetype: B2B Trust Builder
- Goal: Commercial contracts
- Accent: #3b82f6 (blue) | --accent-rgb: 59,130,246
- Hero CTA: "Angebot anfordern"
- Extra section: "Zertifizierungen & Versicherung"
  - Grid of certification badges (placeholders)
  - "Vollstaendig versichert", "ISO 9001", "Meisterbetrieb" etc.
- Extra section: "Referenzen" - Client logo grid (placeholder boxes)
- Testimonials: From FACILITY MANAGERS ("Zuverlaessig seit 5 Jahren...")
- Tone: Corporate, trustworthy, professional. "Sie" form. No slang.
- Icons: building, shield-check, certificate, handshake

## 5. Quality Standards

### Content Quality
- ALL text must be in German.
- No English words mixed in (except technical terms where German equivalent doesn't exist).
- Company name must appear EXACTLY as provided in lead data. No abbreviation, no correction.
- Every service description must be 2-3 sentences of real, useful content. Not "Wir bieten XY an."
  but "Ob Neubau oder Sanierung - wir installieren Ihre Elektrik fachgerecht und nach aktuellen Normen. Von der Planung bis zur Abnahme alles aus einer Hand."
- Testimonials must sound authentic. Use conversational German, not marketing-speak.
  Good: "Hab mich sofort wohlgefuehlt. Super Team, kann ich nur empfehlen."
  Bad: "Exzellenter Service und hoechste Professionalitaet."

### Visual Quality
- Minimum 6 distinct sections with clear visual separation
- At least 3 different SVG icons (not the same icon repeated)
- Gradient glow behind hero content (radial gradient with accent at low opacity)
- Hover effects on ALL interactive elements (buttons, cards, links)
- Consistent spacing: py-20 md:py-32 between sections
- No orphaned text (max-w-2xl or max-w-3xl on paragraphs)

### Technical Quality
- ALL HTML tags must be properly closed
- No duplicate IDs
- All links must have href attributes (use # for placeholders)
- Images: use gradient placeholders with descriptive text, never empty divs
- Minimum HTML file size: 15KB (below this = likely incomplete)
- Mobile menu must actually work (test the JS)

## 6. Validation Checklist (self-check before output)
- [ ] Company name exact from lead data in <title>, h1, footer
- [ ] <title> format: "[Firmenname] - [Kernleistung] in [Stadt]"
- [ ] <meta name="description"> present, < 155 chars, includes city
- [ ] <meta name="robots" content="noindex, nofollow"> present
- [ ] Footer has "Impressum" link
- [ ] Footer has "Datenschutzerklaerung" link
- [ ] No Google Fonts CDN (no fonts.googleapis.com anywhere)
- [ ] Tailwind CDN script present
- [ ] All HTML tags properly closed
- [ ] Mobile menu JS present and functional
- [ ] At least 6 sections with distinct content
- [ ] SVG icons used (not emoji, not unicode symbols)
- [ ] All text in German
- [ ] No lorem ipsum, no "..." placeholders, no "TODO"
- [ ] Star rating matches lead data
- [ ] Phone number from lead data appears on page
- [ ] Industry-specific CTA matches routing table above
- [ ] File size > 15KB
