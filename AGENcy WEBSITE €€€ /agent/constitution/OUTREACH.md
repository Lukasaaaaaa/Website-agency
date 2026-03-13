# OUTREACH.md - Email-Sequenz Vorlagen & Regeln

## Regeln
- NIEMALS Emails automatisch senden. NUR Drafts als .txt Dateien erstellen.
- Jede Email MUSS Absender-Impressum + Opt-Out enthalten.
- Maximal 3 Emails pro Lead. Sequenz: Tag 1, Tag 4, Tag 8.
- Nach 3 Emails ohne Antwort: Stop.

## Absender-Daten
Aus .env: {absender_name}, {stadt}, {impressum}

## Kernprinzip: Pain Points aus Scoring-Daten

Jeder Lead hat messbare Schwächen. Die Email nennt das Problem konkret, nicht generisch. Der Prospect soll denken: "Stimmt, das ist ein Problem."

### Pain Point Hooks (nach Scoring-Signal)

**Keine Website:**
> {firmenname} hat {sterne} Sterne bei Google ({bewertungen} Bewertungen). Aber wenn ein Kunde nach "{nische} in {bezirk}" googelt, findet er Ihre Konkurrenz. Weil die eine Website haben und Sie nicht.

**HTTP only (kein SSL):**
> Mir ist aufgefallen, dass {website_url} noch über HTTP läuft. Seit 2018 zeigt Chrome bei HTTP-Seiten "Nicht sicher" in der Adressleiste. Für Kunden, die zum ersten Mal nach Ihnen suchen, sieht das aus, als wäre Ihre Seite unsicher. Google straft HTTP-Seiten auch im Ranking ab.

**Nicht responsive (nicht mobilfreundlich):**
> Ich habe {website_url} auf dem Handy aufgerufen. Die Seite ist leider nicht mobilfreundlich. 70% Ihrer potenziellen Kunden suchen auf dem Smartphone. Wenn die Seite da nicht funktioniert, rufen die den nächsten an.

**Veraltetes CMS / Copyright-Jahr alt:**
> Ihre Website bei {website_url} scheint seit {copyright_year} nicht aktualisiert worden zu sein. Kunden merken das. Eine veraltete Seite signalisiert: "Dieser Betrieb ist nicht aktiv."

### Nischen-Hooks (nach Branche)

**Handwerker:**
> Junge Leute bewerben sich nicht mehr per Anschreiben. Ein WhatsApp-Button auf Ihrer Website und die Bewerbung dauert 60 Sekunden.

**Physio:**
> Privatpatienten googeln, bevor sie anrufen. Wenn Ihre Seite nicht überzeugt, gehen die zur Praxis nebenan. Online-Terminbuchung ist heute Standard.

**GaLaBau:**
> Ihre besten Projekte sind Ihr Verkaufsargument. Ein Vorher-Nachher-Slider auf der Website überzeugt mehr als jede Visitenkarte.

**Notdienst/Schlüssel:**
> Nachts um 2 googelt jemand panisch "Schlüsseldienst Berlin". Wenn Sie dann nicht mit einem riesigen Anruf-Button auftauchen, ruft er jemand anderen.

**Fahrschule:**
> Fahrschüler sind 17-25 Jahre alt. Die melden sich nicht per Telefon an. Die wollen ein Formular auf dem Handy ausfüllen.

**Gebäudereinigung:**
> Hausverwaltungen und Firmenkunden checken Ihre Website, bevor sie anfragen. Zertifikate, Referenzen, Versicherungsnachweis. Wenn die nicht auf der Seite stehen, kommen Sie gar nicht in die Auswahl.

---

## Email 1: Icebreaker (Tag 1)

Wähle den passenden Pain Point Hook + Nischen-Hook basierend auf den Lead-Daten.

```
Betreff: {firmenname} - {pain_point_betreff}

Hallo {anrede} {nachname},

{pain_point_hook}

Ich bin Webdesigner in Berlin und habe mir erlaubt, einen kostenlosen Website-Entwurf für {firmenname} zu bauen.

Schauen Sie mal rein:
{showcase_url}

{nischen_hook}

Wenn Ihnen der Entwurf gefällt, können wir die Seite in 48 Stunden live schalten. Wenn nicht, kein Problem. Kostet Sie nichts.

Beste Grüße,
{absender_name}

---
{impressum}
Kein Interesse? Antworten Sie kurz mit "Stop".
```

### Betreff-Varianten nach Pain Point
- Keine Website: "Ihre Kunden finden Sie nicht online"
- HTTP only: "Ihre Website zeigt 'Nicht sicher' an"
- Nicht responsive: "Ihre Website funktioniert nicht auf dem Handy"
- Veraltet: "Ihre Website sieht aus wie {copyright_year}"

## Email 2: Bump (Tag 4)
Kurz. Wie vom Handy getippt.

```
Betreff: Re: {firmenname} - {pain_point_betreff}

Hallo {anrede} {nachname},

kurze Frage: Haben Sie den Entwurf gesehen? {showcase_url}

Ich passe ihn gerne an, wenn etwas nicht passt.

Grüße,
{absender_name}
```

## Email 3: Takeaway (Tag 8)
Lösch-Androhung. Höchste Antwortrate.

```
Betreff: Re: {firmenname} - {pain_point_betreff}

Hallo {anrede} {nachname},

da ich nichts gehört habe, lösche ich den Entwurf für {firmenname} am Freitag von meinem Server.

Falls Sie ihn doch behalten möchten, sagen Sie kurz Bescheid.

Viel Erfolg weiterhin,
{absender_name}

---
{impressum}
```

## Draft-Format

```
# DRAFT - NICHT GESENDET
# Lead: {firmenname}
# Pain Point: {pain_point_type}
# Score: {score}
# Template: icebreaker|bump|takeaway
# Geplant: {datum}
# Status: WARTET AUF FREIGABE
# ─────────────────────────────

[Email-Text]
```

## Draft-Dateistruktur
```
out/drafts/{firmenname_slug}/
  email_1_icebreaker.txt
  email_2_bump.txt
  email_3_takeaway.txt
  meta.json
```
