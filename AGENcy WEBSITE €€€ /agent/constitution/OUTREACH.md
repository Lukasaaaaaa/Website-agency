# OUTREACH.md - Email-Sequenz Vorlagen & Regeln

## MANDATORY: Read before drafting ANY outreach.

## Regeln (aus GOVERNANCE.md)
- NIEMALS Emails automatisch senden. NUR Drafts als .txt Dateien erstellen.
- Jede Email MUSS Absender-Impressum enthalten.
- Jede Email MUSS Opt-Out Text enthalten.
- Maximal 3 Emails pro Lead.
- Sequenz-Timing: Tag 1, Tag 4, Tag 8.
- Nach 3 Emails ohne Antwort: Stop, Lead zur Loeschung vormerken.

## Absender-Daten
Die Absender-Daten werden dir im System-Prompt uebergeben (aus .env geladen).
Verwende IMMER die dort angegebenen Werte fuer {absender_name}, {stadt}, {impressum}.

## Nischen-Anpassung
| Nische | Text-Variante fuer "{nische_text}" |
|--------|-------------------------------------|
| Handwerker | Handwerk und Elektrotechnik |
| Physio | Gesundheit und Physiotherapie |
| GaLaBau | Garten- und Landschaftsbau |
| Fahrschule | Fahrschulen |
| Notdienst | Notdienste und Schluesseldienste |
| Reinigung | Gebaeudeservice und Reinigung |

## Email 1: Icebreaker (Tag 1)

```
Betreff: Website-Entwurf fuer {firmenname}

Hallo {anrede} {nachname},

ich bin Webdesigner hier in der Region und mir ist aufgefallen, dass {firmenname} online bei Google Maps sehr gut bewertet ist ({sterne} Sterne, {bewertungen} Bewertungen!), aber die Website dazu aktuell fehlt.

Da ich gerade mein Portfolio im Bereich {nische_text} erweitere, habe ich mir am Wochenende den Spass erlaubt und bereits einen modernen Website-Entwurf speziell fuer Ihren Betrieb gebaut.

Sie koennen sich den Entwurf hier unverbindlich ansehen:
{showcase_url}

Wenn Ihnen das Design gefaellt, lassen Sie es mich einfach wissen. Wir koennten die Seite innerhalb von 48 Stunden genau so fuer Sie live schalten.

Beste Gruesse aus {stadt},
{absender_name}

---
{impressum}
Sie moechten keine weiteren Nachrichten erhalten? Antworten Sie kurz mit "Stop".
```

## Email 2: Bump (Tag 4)

```
Betreff: Re: Website-Entwurf fuer {firmenname}

Hallo {anrede} {nachname},

ich wollte nur kurz nachfragen, ob Sie schon die Gelegenheit hatten, sich den Entwurf unter {showcase_url} anzusehen?

Lassen Sie mich gerne wissen, falls Sie Anpassungswuensche haben oder ob das Design generell in die richtige Richtung geht.

Viele Gruesse,
{absender_name}
```

## Email 3: Takeaway / FOMO (Tag 8)

```
Betreff: Re: Website-Entwurf fuer {firmenname}

Hallo {anrede} {nachname},

da ich bisher nichts von Ihnen gehoert habe, gehe ich davon aus, dass aktuell kein Bedarf fuer den neuen Webauftritt besteht. Das ist voellig in Ordnung!

Ich werde den Entwurf fuer {firmenname} am Freitagabend von meinem Test-Server loeschen, um wieder Speicherplatz fuer neue Projekte freizugeben.

Falls Sie die Seite in Zukunft doch noch nutzen moechten, geben Sie mir einfach kurz vor Freitag Bescheid, dann archiviere ich sie fuer Sie.

Weiterhin viel Erfolg fuer Ihr Geschaeft!

Beste Gruesse,
{absender_name}
```

## Draft-Datei Format

Wenn du einen Draft erstellst, speichere ihn als .txt mit diesem Header:

```
# DRAFT - NICHT GESENDET
# Lead: {firmenname}
# Template: icebreaker|bump|takeaway
# Geplant: {datum}
# Status: WARTET AUF FREIGABE
# ─────────────────────────────

[Email-Text hier]
```

## Draft-Dateistruktur

```
out/drafts/{firmenname_slug}/
  email_1_icebreaker.txt
  email_2_bump.txt
  email_3_takeaway.txt
  meta.json
```

meta.json Beispiel:
```json
{
  "lead_id": "mock_001",
  "firmenname": "Mueller Elektrotechnik",
  "showcase_url": "https://staging.example.com/mueller",
  "created_at": "2026-02-28T14:00:00",
  "status": "pending_approval",
  "sequence": {
    "email_1": { "send_date": "2026-02-28", "template": "icebreaker" },
    "email_2": { "send_date": "2026-03-03", "template": "bump" },
    "email_3": { "send_date": "2026-03-07", "template": "takeaway" }
  }
}
```
