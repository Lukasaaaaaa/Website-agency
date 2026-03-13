# QA Check for websitepolierer.de

You are a QA engineer for the Websitepolierer website. Perform a comprehensive quality assurance check of the live site using WebFetch, compare against local source files, and generate a detailed report.

Run ALL steps below systematically. Use WebFetch for each URL. Read local files for comparison.

## Step 1: Main Page — https://websitepolierer.de

Use WebFetch to load `https://websitepolierer.de` and verify ALL of the following:

**Meta & SEO:**
- Page loads successfully (no errors)
- `<title>` contains "Websitepolierer"
- `<meta name="description">` is present and under 160 characters
- `<meta name="keywords">` is present
- OpenGraph tags exist: `og:title`, `og:description`, `og:type`, `og:url`
- Schema.org JSON-LD is present with `@type: "ProfessionalService"`
- Only ONE `<h1>` tag exists on the page
- Heading hierarchy is correct (h1 → h2 → h3, no skips)

**Structure & Content:**
- All section IDs exist: `hero`, `leistungen`, `branchen`, `ablauf`, `preise`, `faq`, `ueber`, `kontakt`
- Navigation contains links to all sections
- Contact email is `lukas@websitepolierer.de`
- Footer contains links to Impressum and Datenschutz
- Footer contains links to all 5 demo pages
- Pricing shows: 1.500 (website), 79 (maintenance), 299 (SEO)
- 3 testimonial cards are present in social proof section
- 5 Branchen cards are present
- 9 FAQ items exist (count `<details>` elements)

**Forms & Interactive:**
- Contact form exists with `id="contactForm"`
- Form has name, email, and message fields
- Submit button is present

## Step 2: Legal Pages

**Impressum** — Use WebFetch on `https://websitepolierer.de/impressum.html`:
- Page loads with content
- Contains "Impressum" heading
- Contains address: Braillestraße 4, 12165 Berlin
- Has `noindex` meta tag
- Has navigation link back to main page

**Datenschutz** — Use WebFetch on `https://websitepolierer.de/datenschutz.html`:
- Page loads with content
- Contains "Datenschutz" heading
- Has `noindex` meta tag
- Has navigation link back to main page

## Step 3: Demo Pages

Use WebFetch on each URL and verify it loads with content and has `noindex, nofollow`:
1. `https://websitepolierer.de/demos/handwerker.html`
2. `https://websitepolierer.de/demos/gartenbau.html`
3. `https://websitepolierer.de/demos/praxis.html`
4. `https://websitepolierer.de/demos/notdienst.html`
5. `https://websitepolierer.de/demos/dienstleister.html`

For each, verify:
- Page loads with content (not empty/error)
- Has `noindex, nofollow` meta robots tag
- References Inter font from `../assets/fonts/`

## Step 4: Assets

Use WebFetch to verify these assets are accessible:
- `https://websitepolierer.de/assets/logo.svg`
- `https://websitepolierer.de/assets/inhaber.jpg`
- `https://websitepolierer.de/style.css`
- `https://websitepolierer.de/script.js`

## Step 5: Local vs. Live Comparison

Read the local files at `website/index.html`, `website/style.css`, `website/script.js` and compare key content against the WebFetch results:
- Compare the `<title>` tag text
- Compare the hero heading text
- Compare pricing amounts (1.500, 79, 299)
- Compare contact email
- Compare number of FAQ items
- Compare number of demo page links
- **Flag any discrepancies** between local and live

## Step 6: Link Integrity

From the main page WebFetch results:
- List all internal links (href starting with # or relative paths)
- Verify anchor links (#leistungen, #branchen, etc.) have matching section IDs
- Verify demo page links point to valid paths in `/demos/`
- Verify legal page links point to valid paths
- Flag any broken or suspicious links

## Step 7: Generate Report

Output a structured report with these sections:

### PASS (items that checked out)
Use checkmarks for each passing item, grouped by step.

### FAIL (items that failed)
Use X marks, include details on what was expected vs. what was found.

### WARN (items that need attention but aren't broken)
Include things like:
- Contact form has no backend (action="#")
- Any content that looks outdated
- Any images without alt text
- Performance concerns

### RECOMMENDATIONS
Suggest improvements found during the QA process:
- SEO improvements
- Accessibility improvements
- Content updates needed
- Missing features or broken interactions

### SYNC STATUS
Clearly state whether the live site matches the local codebase, or if a deployment is needed.
