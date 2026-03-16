#!/usr/bin/env python3
"""
Robust Batch-Scraper: ALLE Tiers — Berlin + Brandenburg.
- Skips already-scraped query+location combos
- Catches per-query errors without crashing
- Saves after every query
- Includes Tier 3 (Sonstige lokale Betriebe)
"""

import json, time, sys, traceback
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from scraper import search_google_maps

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
OUTPUT = DATA / "all_leads.json"

# ══════════════════════════════════════════════════════════════
#  ALLE Branchen
# ══════════════════════════════════════════════════════════════

BRANCHEN = {
    "Handwerk & Bau": [
        "Zimmermann", "Trockenbau", "Estrichleger", "Gerüstbau",
        "Glaserei", "Stuckateur", "Steinmetz", "Metallbau",
        "Rolladenbau", "Parkett verlegen", "Maurer",
    ],
    "Energie & Solar": [
        "Solaranlage Installation", "Photovoltaik Installateur",
        "Wärmepumpe Installation", "Klimaanlage Monteur",
        "Energieberater", "Wallbox Installation",
        "Solarthermie", "Pelletheizung Installation",
    ],
    "Ingenieurbüros & Gutachter": [
        "Ingenieurbüro", "Architekturbüro", "Statiker",
        "Vermessungsbüro", "Baugutachter", "Immobiliengutachter",
        "Sachverständiger Bau", "Energieausweis Aussteller",
        "Brandschutzgutachter", "KFZ Gutachter",
    ],
    "Sonstige lokale Betriebe": [
        "Restaurant", "Café", "Imbiss", "Catering", "Foodtruck",
        "Reifenwechsel", "Autolackierer", "Smart Repair Auto",
        "Motorrad Werkstatt",
        "Änderungsschneiderei", "Textilreinigung",
        "Hundesalon", "Hundeschule",
        "Fotograf", "Hochzeitsfotograf",
        "Tattoo Studio", "Piercing Studio",
        "Yogastudio", "Fitnessstudio",
        "Tanzschule", "Musikschule", "Nachhilfe",
        "Reinigung Büro", "Schädlingsbekämpfung",
        "Bestatter", "Entrümpelung",
        "Schlosserei Kunstschmiede", "Polsterei",
        "Goldschmied", "Uhrmacher",
    ],
}

STANDORTE = [
    "Berlin",
    "Potsdam",
    "Cottbus",
    "Brandenburg an der Havel",
    "Frankfurt Oder",
    "Oranienburg",
    "Falkensee",
    "Bernau bei Berlin",
    "Königs Wusterhausen",
]

# ══════════════════════════════════════════════════════════════

def load_existing():
    if OUTPUT.exists():
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    return []

def save_leads(leads):
    # Atomic write via temp file
    tmp = OUTPUT.with_suffix('.tmp')
    tmp.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.rename(OUTPUT)

def dedup_key(lead):
    return f"{lead.get('name','').lower().strip()}|{lead.get('address','').lower().strip()}"

def get_done_combos(leads):
    """Which query+location combos are already scraped?"""
    return {f"{l.get('query','')}|{l.get('location','')}" for l in leads if l.get('tier')}

def main():
    existing = load_existing()
    seen = {dedup_key(l) for l in existing}
    all_leads = list(existing)
    done_combos = get_done_combos(existing)
    
    total_new = 0
    total_queries = 0
    skipped = 0
    errors = 0
    
    all_combos = []
    for tier_name, branchen in BRANCHEN.items():
        for branche in branchen:
            for stadt in STANDORTE:
                all_combos.append((tier_name, branche, stadt))
    
    # Filter out already done
    todo = [(t, b, s) for t, b, s in all_combos if f"{b}|{s}" not in done_combos]
    
    print(f"\n{'='*60}")
    print(f"  BATCH SCRAPE — ALLE TIERS")
    print(f"  Total Combos:    {len(all_combos)}")
    print(f"  Bereits fertig:  {len(all_combos) - len(todo)}")
    print(f"  Noch zu scrapen: {len(todo)}")
    print(f"  Bestehende Leads: {len(existing)}")
    print(f"  Start: {datetime.now():%H:%M:%S}")
    print(f"{'='*60}\n", flush=True)
    
    for i, (tier_name, branche, stadt) in enumerate(todo):
        total_queries += 1
        query_label = f"[{i+1}/{len(todo)}] {branche} in {stadt} ({tier_name})"
        
        try:
            print(f"\n{query_label}", flush=True)
            result = search_google_maps(branche, stadt, max_results=15)
            
            new_count = 0
            for lead in result.get("results", []):
                lead["query"] = branche
                lead["location"] = stadt
                lead["tier"] = tier_name
                lead["scraped_at"] = datetime.now().isoformat()
                
                key = dedup_key(lead)
                if key not in seen:
                    seen.add(key)
                    all_leads.append(lead)
                    new_count += 1
            
            total_new += new_count
            found = result.get('total_found', 0)
            print(f"  → {found} gefunden, {new_count} neu (total: {len(all_leads)})", flush=True)
            
            # Save after EVERY query for robustness
            save_leads(all_leads)
            
            # Rate limiting
            wait = 4 + (i % 3)
            time.sleep(wait)
            
        except KeyboardInterrupt:
            print("\n\n  ⏹ Abgebrochen. Leads gespeichert.")
            save_leads(all_leads)
            break
        except Exception as e:
            errors += 1
            print(f"  ❌ FEHLER: {e}", flush=True)
            traceback.print_exc()
            save_leads(all_leads)
            time.sleep(8)  # longer wait after error
            continue
    
    save_leads(all_leads)
    
    # Final stats
    print(f"\n{'='*60}")
    print(f"  FERTIG")
    print(f"  Queries:     {total_queries}")
    print(f"  Neue Leads:  {total_new}")
    print(f"  Total Leads: {len(all_leads)}")
    print(f"  Fehler:      {errors}")
    print(f"  Ende:        {datetime.now():%H:%M:%S}")
    print(f"{'='*60}\n")
    
    # Stats by tier
    for tier_name in BRANCHEN:
        tier_leads = [l for l in all_leads if l.get("tier") == tier_name]
        no_web = len([l for l in tier_leads if not l.get("website")])
        print(f"  {tier_name}: {len(tier_leads)} Leads ({no_web} ohne Website)")
    
    # Old leads (no tier)
    old = [l for l in all_leads if not l.get("tier")]
    no_web_old = len([l for l in old if not l.get("website")])
    print(f"  (Bestand): {len(old)} Leads ({no_web_old} ohne Website)")
    print(f"\n  GESAMT: {len(all_leads)} Leads ({len([l for l in all_leads if not l.get('website')])} ohne Website)")

if __name__ == "__main__":
    main()
