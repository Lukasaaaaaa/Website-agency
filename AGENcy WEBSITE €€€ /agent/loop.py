#!/usr/bin/env python3
"""
OpenClaw (German Edition) - Autonomer Web-Design-Sales-Agent
Constitution-MDs = Gehirn. Dieser Loop = Koerper.
"""

import os, sys, json, time, logging, random, re, subprocess, shutil
from datetime import datetime, timedelta
from pathlib import Path

# .env laden (falls python-dotenv installiert)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

import anthropic

# ══════════════════════════════════════════════════════════════
#  Pfade
# ══════════════════════════════════════════════════════════════

BASE = Path(__file__).parent
CONSTITUTION = BASE / "constitution"
DATA = BASE / "data"
OUT_SITES = BASE / "out" / "sites"
OUT_DRAFTS = BASE / "out" / "drafts"
LOGS = BASE / "logs"
QUEUE_FILE = DATA / "approval_queue.json"
COST_FILE = DATA / f"costs_{datetime.now():%Y-%m-%d}.json"

for d in [DATA, OUT_SITES, OUT_DRAFTS, LOGS]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOGS / f"{datetime.now():%Y-%m-%d}.log"), logging.StreamHandler()]
)
log = logging.getLogger("openclaw")

# ══════════════════════════════════════════════════════════════
#  Kosten-Tracking
# ══════════════════════════════════════════════════════════════

# Preise pro 1M Tokens (Sonnet 4, Stand Feb 2026)
PRICE_INPUT = 3.00 / 1_000_000
PRICE_OUTPUT = 15.00 / 1_000_000

def track_cost(usage):
    """Speichert Token-Verbrauch und geschaetzte Kosten."""
    inp = getattr(usage, "input_tokens", 0)
    out = getattr(usage, "output_tokens", 0)
    cost = inp * PRICE_INPUT + out * PRICE_OUTPUT

    data = json.loads(COST_FILE.read_text()) if COST_FILE.exists() else {"total_eur": 0, "calls": 0, "input_tokens": 0, "output_tokens": 0}
    data["total_eur"] = round(data["total_eur"] + cost, 4)
    data["calls"] += 1
    data["input_tokens"] += inp
    data["output_tokens"] += out
    COST_FILE.write_text(json.dumps(data, indent=2))
    return data["total_eur"]

def check_budget():
    """Prueft ob Tagesbudget ueberschritten."""
    budget = float(os.environ.get("DAILY_BUDGET_EUR", "5.00"))
    if not COST_FILE.exists():
        return True
    data = json.loads(COST_FILE.read_text())
    if data["total_eur"] >= budget:
        log.warning(f"Budget erreicht: {data['total_eur']:.2f} EUR >= {budget:.2f} EUR")
        return False
    return True

# ══════════════════════════════════════════════════════════════
#  DSGVO-Loeschung
# ══════════════════════════════════════════════════════════════

def run_dsgvo_cleanup():
    """Loescht Leads + Websites aelter als 14 Tage ohne Freigabe."""
    if not QUEUE_FILE.exists():
        return
    queue = json.loads(QUEUE_FILE.read_text())
    cutoff = datetime.now() - timedelta(days=14)
    kept, deleted = [], 0

    for entry in queue:
        ts = entry.get("queued_at") or entry.get("approved_at", "")
        try:
            entry_date = datetime.fromisoformat(ts)
        except (ValueError, TypeError):
            kept.append(entry)
            continue

        # Nur ausstehende/abgelehnte Leads aelter als 14 Tage loeschen
        if entry.get("status") in ("pending", "rejected", "skipped") and entry_date < cutoff:
            # Website-Datei loeschen
            wp = entry.get("website_path", "")
            if wp and Path(wp).exists():
                Path(wp).unlink()
                log.info(f"DSGVO: Geloescht {wp}")
            # Draft-Ordner loeschen
            dd = entry.get("drafts_dir", "")
            if dd and Path(dd).exists():
                shutil.rmtree(Path(dd))
                log.info(f"DSGVO: Geloescht {dd}")
            deleted += 1
        else:
            kept.append(entry)

    QUEUE_FILE.write_text(json.dumps(kept, indent=2, ensure_ascii=False))
    if deleted:
        log.info(f"DSGVO-Cleanup: {deleted} Eintraege geloescht")

# ══════════════════════════════════════════════════════════════
#  Constitution laden
# ══════════════════════════════════════════════════════════════

def load_constitution():
    order = ["GOVERNANCE.md", "SCORING.md", "SPECS.md", "OUTREACH.md", "VALIDATION.md", "TOOLS.md", "AGENTS.md"]
    parts = []
    for name in order:
        f = CONSTITUTION / name
        if f.exists():
            parts.append(f"# === {name} ===\n{f.read_text()}")
    return "\n\n".join(parts)

# ══════════════════════════════════════════════════════════════
#  Absender-Daten aus .env
# ══════════════════════════════════════════════════════════════

def get_absender():
    return {
        "name": os.environ.get("ABSENDER_NAME", "[DEIN NAME]"),
        "email": os.environ.get("ABSENDER_EMAIL", "[DEINE EMAIL]"),
        "telefon": os.environ.get("ABSENDER_TELEFON", "[DEINE NUMMER]"),
        "stadt": os.environ.get("ABSENDER_STADT", "[DEINE STADT]"),
        "impressum": os.environ.get("ABSENDER_IMPRESSUM", "[IMPRESSUM]").replace("\\n", "\n"),
    }

# ══════════════════════════════════════════════════════════════
#  Tools
# ══════════════════════════════════════════════════════════════

TOOLS = [
    {"name": "search_google_maps", "description": "Search Google Maps for local businesses.",
     "input_schema": {"type": "object", "properties": {
         "query": {"type": "string"}, "location": {"type": "string"}
     }, "required": ["query", "location"]}},

    {"name": "check_url", "description": "Check if a website exists and its quality.",
     "input_schema": {"type": "object", "properties": {
         "url": {"type": "string"}
     }, "required": ["url"]}},

    {"name": "save_file", "description": "Save content to a file.",
     "input_schema": {"type": "object", "properties": {
         "path": {"type": "string", "description": "Relative to agent dir, e.g. out/sites/name.html"},
         "content": {"type": "string"}
     }, "required": ["path", "content"]}},

    {"name": "read_file", "description": "Read a file.",
     "input_schema": {"type": "object", "properties": {
         "path": {"type": "string"}
     }, "required": ["path"]}},

    {"name": "deploy_site", "description": "Deploy an HTML file to Netlify. Returns the live URL.",
     "input_schema": {"type": "object", "properties": {
         "html_path": {"type": "string", "description": "Relative path to the HTML file, e.g. out/sites/mueller.html"},
         "subdirectory": {"type": "string", "description": "URL path on the site, e.g. mueller-elektrotechnik"}
     }, "required": ["html_path"]}},

    {"name": "request_human_approval", "description": "Pause and ask the human to approve this lead. Returns approved/rejected.",
     "input_schema": {"type": "object", "properties": {
         "firmenname": {"type": "string"},
         "score": {"type": "integer"},
         "website_path": {"type": "string"},
         "showcase_url": {"type": "string", "description": "Live URL after deployment"},
         "email_preview": {"type": "string", "description": "First lines of the icebreaker email"},
         "summary": {"type": "string"}
     }, "required": ["firmenname", "score", "website_path", "summary"]}},

    {"name": "log", "description": "Write a log entry.",
     "input_schema": {"type": "object", "properties": {
         "level": {"type": "string", "enum": ["info", "warning", "error"]},
         "message": {"type": "string"}
     }, "required": ["level", "message"]}},
]

def execute_tool(name, args):
    try:
        if name == "search_google_maps":
            return _search(args["query"], args["location"])
        elif name == "check_url":
            return _check_url(args["url"])
        elif name == "save_file":
            p = BASE / args["path"]
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"], encoding="utf-8")
            return json.dumps({"saved": True, "path": str(p), "size": len(args["content"])})
        elif name == "read_file":
            p = BASE / args["path"]
            return p.read_text(encoding="utf-8") if p.exists() else json.dumps({"error": "not found"})
        elif name == "deploy_site":
            return _deploy_netlify(args)
        elif name == "request_human_approval":
            return _hitl_prompt(args)
        elif name == "log":
            getattr(log, args.get("level", "info"))(args["message"])
            return json.dumps({"logged": True})
        return json.dumps({"error": f"unknown tool: {name}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ══════════════════════════════════════════════════════════════
#  Netlify Deployment
# ══════════════════════════════════════════════════════════════

def _deploy_netlify(args):
    """Deployed eine HTML-Datei auf Netlify."""
    token = os.environ.get("NETLIFY_TOKEN")
    site_id = os.environ.get("NETLIFY_SITE_ID")
    html_path = BASE / args["html_path"]

    if not token:
        return json.dumps({"error": "NETLIFY_TOKEN nicht gesetzt in .env", "url": None})
    if not html_path.exists():
        return json.dumps({"error": f"Datei nicht gefunden: {html_path}", "url": None})

    # Netlify Deploy API: einzelne Datei als Site deployen
    # Erstelle temporaeres Verzeichnis mit der HTML-Datei
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        subdir = args.get("subdirectory", html_path.stem)
        target = Path(tmpdir) / "index.html"
        shutil.copy2(html_path, target)

        try:
            # netlify-cli deploy
            cmd = ["netlify", "deploy", "--prod", "--dir", tmpdir]
            if site_id:
                cmd += ["--site", site_id]
            env = {**os.environ, "NETLIFY_AUTH_TOKEN": token}
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)

            if result.returncode == 0:
                # URL aus Output parsen
                url_match = re.search(r'(https://[^\s]+\.netlify\.app[^\s]*)', result.stdout)
                url = url_match.group(1) if url_match else f"https://{site_id}.netlify.app"
                log.info(f"Deployed: {html_path.name} -> {url}")
                return json.dumps({"deployed": True, "url": url})
            else:
                return json.dumps({"error": result.stderr[:300], "url": None})
        except FileNotFoundError:
            # Fallback: Netlify API direkt via requests
            try:
                import requests
                # Zip das Verzeichnis
                import zipfile, io
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zf:
                    zf.write(target, "index.html")
                zip_buffer.seek(0)

                headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/zip"}
                endpoint = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys" if site_id else "https://api.netlify.com/api/v1/sites"
                resp = requests.post(endpoint, headers=headers, data=zip_buffer.read(), timeout=30)

                if resp.status_code in (200, 201):
                    data = resp.json()
                    url = data.get("ssl_url") or data.get("url") or f"https://{site_id}.netlify.app"
                    log.info(f"Deployed via API: {html_path.name} -> {url}")
                    return json.dumps({"deployed": True, "url": url})
                else:
                    return json.dumps({"error": resp.text[:300], "url": None})
            except ImportError:
                return json.dumps({"error": "Weder netlify-cli noch requests installiert", "url": None})

# ══════════════════════════════════════════════════════════════
#  HITL
# ══════════════════════════════════════════════════════════════

def _hitl_prompt(args):
    print("\n" + "=" * 60)
    print("  FREIGABE ERFORDERLICH")
    print("=" * 60)
    print(f"  Firma:    {args.get('firmenname', '?')}")
    print(f"  Score:    {args.get('score', '?')}/100")
    print(f"  Website:  {args.get('website_path', '?')}")
    if args.get("showcase_url"):
        print(f"  Live URL: {args['showcase_url']}")
    print(f"  Summary:  {args.get('summary', '?')}")
    if args.get("email_preview"):
        print(f"\n  Email-Vorschau:\n  {args['email_preview'][:400]}")
    print("=" * 60)

    while True:
        answer = input("  Freigeben? [Y]es / [N]o / [S]kip: ").strip().upper()
        if answer in ("Y", "YES", "J", "JA"):
            q = json.loads(QUEUE_FILE.read_text()) if QUEUE_FILE.exists() else []
            q.append({
                "firmenname": args.get("firmenname"), "score": args.get("score"),
                "website_path": args.get("website_path"), "showcase_url": args.get("showcase_url", ""),
                "approved_at": datetime.now().isoformat(), "status": "approved"
            })
            QUEUE_FILE.write_text(json.dumps(q, indent=2, ensure_ascii=False))
            log.info(f"APPROVED: {args.get('firmenname')}")
            return json.dumps({"approved": True, "action": "approved"})
        elif answer in ("N", "NO", "NEIN"):
            reason = input("  Grund (optional): ").strip()
            log.info(f"REJECTED: {args.get('firmenname')} - {reason}")
            return json.dumps({"approved": False, "action": "rejected", "reason": reason})
        elif answer in ("S", "SKIP"):
            log.info(f"SKIPPED: {args.get('firmenname')}")
            return json.dumps({"approved": False, "action": "skipped"})
        print("  Bitte Y, N oder S eingeben.")

# ══════════════════════════════════════════════════════════════
#  Search
# ══════════════════════════════════════════════════════════════

def _search(query, location):
    # Try SerpAPI first if key exists
    key = os.environ.get("SERPAPI_KEY")
    if key:
        try:
            import serpapi
            r = serpapi.search({"engine": "google_maps", "q": f"{query} in {location}", "hl": "de", "gl": "de", "api_key": key})
            results = [{"name": x.get("title",""), "address": x.get("address",""), "phone": x.get("phone"),
                        "rating": x.get("rating",0), "review_count": x.get("reviews",0),
                        "website": x.get("website"), "place_id": x.get("place_id",""),
                        "category": x.get("type","")} for x in r.get("local_results", [])[:20]]
            return json.dumps({"results": results, "total_found": len(results), "source": "serpapi"}, ensure_ascii=False)
        except Exception as e:
            log.warning(f"SerpAPI failed: {e}, falling back to Playwright")

    # Fallback: Playwright scraper (real Google Maps data)
    try:
        from scraper import search_google_maps
        result = search_google_maps(query, location, max_results=15)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        log.error(f"Playwright scraper failed: {e}")
        return json.dumps({"results": [], "error": str(e), "source": "playwright_error"}, ensure_ascii=False)

# ══════════════════════════════════════════════════════════════
#  URL Check
# ══════════════════════════════════════════════════════════════

def _check_url(url):
    if not url or url.upper() in ("FEHLT", "NONE", "N/A", ""):
        return json.dumps({"exists": False, "status": "missing"})
    try:
        import requests
        r = requests.head(url, timeout=10, allow_redirects=True)
        if r.status_code >= 400:
            return json.dumps({"exists": False, "status": "broken", "status_code": r.status_code})
        full = requests.get(url, timeout=15).text.lower()
        cms = next((c for k, c in [("wp-content","WordPress"),("squarespace","Squarespace"),("wix.com","Wix"),("jimdo","Jimdo")] if k in full), None)
        responsive = "viewport" in full and "width=device-width" in full
        ssl = url.startswith("https://")
        yr = re.search(r'(?:copyright|©|\(c\))\s*(\d{4})', full)
        modern = ssl and responsive and cms and yr and int(yr.group(1)) >= 2023
        return json.dumps({"exists": True, "is_responsive": responsive, "has_ssl": ssl, "cms": cms,
                           "copyright_year": int(yr.group(1)) if yr else None, "status": "modern" if modern else "outdated"})
    except Exception as e:
        return json.dumps({"exists": False, "status": "error", "error": str(e)})

# ══════════════════════════════════════════════════════════════
#  Agent Loop
# ══════════════════════════════════════════════════════════════

TARGETS = [
    {"niche": "Elektriker", "locations": ["Berlin", "Potsdam", "Hamburg"]},
    {"niche": "Maler", "locations": ["Berlin", "Muenchen", "Koeln"]},
    {"niche": "Dachdecker", "locations": ["Berlin", "Frankfurt", "Stuttgart"]},
    {"niche": "Physiotherapie", "locations": ["Berlin", "Hamburg", "Muenchen"]},
    {"niche": "Garten und Landschaftsbau", "locations": ["Berlin", "Potsdam", "Dresden"]},
]

def run():
    # Budget-Check
    if not check_budget():
        print("  Tagesbudget erreicht. Zyklus uebersprungen.")
        return

    # DSGVO-Cleanup am Start jedes Zyklus
    run_dsgvo_cleanup()

    client = anthropic.Anthropic()
    constitution = load_constitution()
    absender = get_absender()
    target = random.choice(TARGETS)
    location = random.choice(target["locations"])
    max_leads = int(os.environ.get("MAX_LEADS_PER_CYCLE", "5"))

    print(f"\n{'=' * 60}")
    print(f"  OpenClaw - Zyklus gestartet")
    print(f"  Suche: {target['niche']} in {location}")
    print(f"  Zeit:  {datetime.now():%Y-%m-%d %H:%M}")
    print(f"{'=' * 60}\n")

    system = f"""Du bist OpenClaw (German Edition), ein autonomer Web-Design-Sales-Agent.

DEINE CONSTITUTION (du MUSST diese Regeln befolgen):
{constitution}

ABSENDER-DATEN (fuer Outreach-Emails):
Name: {absender['name']}
Email: {absender['email']}
Telefon: {absender['telefon']}
Stadt: {absender['stadt']}
Impressum:
{absender['impressum']}

DIESER ZYKLUS:
Suche nach: {target['niche']} in {location}

WORKFLOW (nach AGENTS.md):
1. search_google_maps aufrufen
2. Fuer jedes Ergebnis: check_url falls Website vorhanden, dann Lead scoren (im Kopf, nach SCORING.md)
3. Qualifizierte Leads (Score >= 40): Website generieren (im Kopf nach SPECS.md), mit save_file speichern
4. Generiertes HTML selbst validieren (nach VALIDATION.md), bei Fehler korrigieren (max 3x)
5. deploy_site aufrufen um die Website live zu schalten
6. Outreach-Drafts erstellen (nach OUTREACH.md) mit den echten Absender-Daten oben, mit save_file speichern
7. request_human_approval aufrufen -- HARD STOP, niemals ueberspringen

DENKE LAUT: Erklaere bei jedem Schritt kurz was du tust und warum.
Maximal {max_leads} Leads pro Zyklus. NIEMALS Emails senden, nur Drafts."""

    messages = [{"role": "user", "content": "Starte den Agent-Zyklus."}]
    log.info(f"=== Zyklus: {target['niche']} in {location} ===")

    for turn in range(30):
        if not check_budget():
            log.warning("Budget mid-cycle erreicht, stoppe.")
            break

        resp = client.messages.create(
            model=os.environ.get("OPENCLAW_MODEL", "claude-sonnet-4-20250514"),
            max_tokens=16000, system=system, tools=TOOLS, messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})

        # Kosten tracken
        total_eur = track_cost(resp.usage)
        log.info(f"Turn {turn+1} | Kosten heute: {total_eur:.3f} EUR")

        # Sichtbares Denken
        for block in resp.content:
            if hasattr(block, "text") and block.text.strip():
                print(f"\n  [OpenClaw denkt]\n  {block.text[:500]}\n")

        tool_calls = [b for b in resp.content if b.type == "tool_use"]
        if not tool_calls:
            log.info("Zyklus beendet.")
            break

        results = []
        for tc in tool_calls:
            log.info(f"Tool: {tc.name}")
            print(f"  -> {tc.name}({json.dumps(tc.input, ensure_ascii=False)[:80]})")
            result = execute_tool(tc.name, tc.input)
            results.append({"type": "tool_result", "tool_use_id": tc.id, "content": result})
        messages.append({"role": "user", "content": results})

    # Kosten-Summary
    if COST_FILE.exists():
        costs = json.loads(COST_FILE.read_text())
        print(f"\n  Kosten heute: {costs['total_eur']:.3f} EUR ({costs['calls']} API-Calls)")

    print(f"\n{'=' * 60}")
    print(f"  OpenClaw - Zyklus beendet")
    print(f"{'=' * 60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="OpenClaw (German Edition)")
    p.add_argument("--once", action="store_true", help="Einmal ausfuehren und beenden")
    p.add_argument("--interval", type=int, default=3600, help="Sekunden zwischen Zyklen")
    p.add_argument("--cleanup-only", action="store_true", help="Nur DSGVO-Cleanup ausfuehren")
    a = p.parse_args()

    if a.cleanup_only:
        run_dsgvo_cleanup()
        print("DSGVO-Cleanup abgeschlossen.")
    elif a.once:
        run()
    else:
        while True:
            try:
                run()
            except KeyboardInterrupt:
                print("\nOpenClaw gestoppt.")
                break
            except Exception as e:
                log.error(f"Crash: {e}")
                time.sleep(60)
                continue
            time.sleep(a.interval)
