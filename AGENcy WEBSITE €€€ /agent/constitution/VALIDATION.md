# VALIDATION.md - Website-Qualitaetspruefung

## MANDATORY: After EVERY website generation, run through this checklist.
## If ANY critical check fails: fix it or regenerate. Max 3 Versuche.

## Kritische Checks (Fehler = MUSS behoben werden)

1. **Impressum-Link**: Footer muss "Impressum" enthalten
2. **Datenschutz-Link**: Footer muss "Datenschutzerklaerung" enthalten
3. **Firmenname im Title**: `<title>` muss den exakten Firmennamen enthalten
4. **Kein Google Fonts**: Nirgendwo `fonts.googleapis.com` oder `fonts.gstatic.com`
5. **noindex Meta**: `<meta name="robots" content="noindex, nofollow">` vorhanden
6. **Tailwind CDN**: `cdn.tailwindcss.com` im HTML
7. **HTML valide**: Alle Tags korrekt geschlossen (kein offenes `<div>` ohne `</div>`)
8. **Viewport Meta**: `<meta name="viewport" ...>` vorhanden

## Qualitaets-Checks (Warnung, aber kein Blocker)

9. **Dateigrösse**: HTML > 15KB (darunter = wahrscheinlich unvollstaendig)
10. **Sektionen**: Mindestens 6 sichtbare Sektionen (Nav, Hero, Leistungen, Ueber uns, Bewertungen, Footer)
11. **SVG Icons**: Mindestens 3 verschiedene SVG-Icons (nicht dasselbe Icon wiederholt)
12. **Keine Platzhalter**: Kein "Lorem ipsum", kein "...", kein "TODO", kein "FIXME"
13. **Alles Deutsch**: Kein englischer Text in Sichtbereichen
14. **Telefonnummer**: Wenn vorhanden, muss sie im HTML auftauchen
15. **Stern-Bewertung**: Muss mit den Lead-Daten uebereinstimmen
16. **Branchenspezifischer CTA**: Muss zum Industry Routing in SPECS.md passen

## Automatische Reparaturen

Diese Probleme kannst du selbst fixen ohne neu zu generieren:

- **noindex fehlt**: Fuege `<meta name="robots" content="noindex, nofollow">` in `<head>` ein
- **Google Fonts gefunden**: Entferne alle `<link>` Tags mit `fonts.googleapis.com` und ersetze `@import url(...)` mit `/* removed */`

## Self-Correction Protokoll

1. Generiere Website
2. Pruefe alle Checks oben
3. Wenn kritischer Fehler:
   - Versuch 1: Automatische Reparatur (noindex, Google Fonts)
   - Versuch 2: Regeneriere mit explizitem Hinweis auf den Fehler
   - Versuch 3: Regeneriere mit SPECS.md nochmal komplett neu gelesen
   - Nach 3 Versuchen: Lead ueberspringen, Fehler loggen, zur Eskalation melden
