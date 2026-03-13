# TOOLS.md - Verfuegbare Werkzeuge

## Ueberblick

Du hast Zugriff auf diese minimalen Werkzeuge. Alles andere (Scoring, Validierung,
Website-Generierung, Outreach-Texte) machst du SELBST durch Nachdenken und die
Regeln in den anderen Constitution-Files.

## Tool: search_google_maps

Sucht auf Google Maps nach lokalen Unternehmen.

**Input:**
- `query` (string): Branche, z.B. "Elektriker", "Physiotherapie"
- `location` (string): Stadt oder PLZ, z.B. "Berlin", "10115"

**Output:**
```json
{
  "results": [
    {
      "name": "Firmenname",
      "address": "Strasse, PLZ Stadt",
      "phone": "0170-1234567",
      "rating": 4.6,
      "review_count": 14,
      "website": null,
      "place_id": "ChIJ...",
      "category": "Elektriker"
    }
  ],
  "total_found": 3,
  "source": "serpapi"
}
```

## Tool: check_url

Prueft ob eine Website existiert und wie modern sie ist.

**Input:**
- `url` (string): Die URL

**Output:**
```json
{
  "exists": true,
  "status_code": 200,
  "is_responsive": true,
  "has_ssl": true,
  "cms": "WordPress",
  "copyright_year": 2024,
  "status": "modern"
}
```

Status-Werte: "missing", "broken", "timeout", "outdated", "modern"

## Tool: save_file

Speichert eine Datei auf der Festplatte.

**Input:**
- `path` (string): Dateipfad relativ zum Agent-Verzeichnis, z.B. "out/sites/mueller_elektrotechnik.html"
- `content` (string): Dateiinhalt

**Output:** `{ "saved": true, "path": "...", "size": 12345 }`

## Tool: read_file

Liest eine Datei von der Festplatte.

**Input:**
- `path` (string): Dateipfad

**Output:** Dateiinhalt als String

## Tool: deploy_site

Deployed eine HTML-Datei auf Netlify. Gibt die live URL zurueck.

**Input:**
- `html_path` (string): Relativer Pfad zur HTML-Datei, z.B. "out/sites/mueller.html"
- `subdirectory` (string, optional): URL-Pfad auf der Site

**Output:** `{ "deployed": true, "url": "https://dein-staging.netlify.app" }`

WICHTIG: Rufe deploy_site NACH save_file und Validierung auf, BEVOR du request_human_approval aufrufst.
So hat der Mensch eine echte URL zum Ansehen.

## Tool: request_human_approval

Pausiert den Agent und fragt den Menschen im Terminal um Freigabe.

**Input:**
- `firmenname` (string)
- `score` (integer)
- `website_path` (string)
- `showcase_url` (string): Die Live-URL nach Deployment
- `email_preview` (string): Erste Zeilen der Icebreaker-Email
- `summary` (string): 1-2 Saetze zum Lead

**Output:** `{ "approved": true/false, "action": "approved/rejected/skipped" }`

HARD STOP: Du MUSST dieses Tool fuer JEDEN Lead aufrufen bevor du zum naechsten weitergehst.

## Tool: log

Schreibt einen Logeintrag.

**Input:**
- `level` (string): "info", "warning", "error"
- `message` (string)

**Output:** `{ "logged": true }`

## Was du OHNE Tools machst

Diese Aufgaben loest du durch Nachdenken, NICHT durch Tool-Aufrufe:

- **Lead Scoring**: Lies SCORING.md, wende die Regeln auf die Search-Ergebnisse an, berechne den Score im Kopf
- **Website Generierung**: Lies SPECS.md, generiere das komplette HTML selbst als String, speichere es mit save_file
- **Outreach Drafts**: Lies OUTREACH.md, fuelle die Templates mit Lead-Daten und den Absender-Daten aus dem System-Prompt, speichere mit save_file
- **Validierung**: Lies VALIDATION.md, pruefe dein generiertes HTML gegen die Checkliste
- **Nischen-Klassifizierung**: Ordne die Google Maps Kategorie einer Nische zu (Handwerker, Physio, GaLaBau, Fahrschule, Notdienst, Reinigung)
