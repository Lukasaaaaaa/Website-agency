#!/usr/bin/env python3
"""
Batch-Scraper Tier 3: Sonstige lokale Betriebe — Berlin + Brandenburg.
Speichert in data/all_leads.json (append, dedupliziert).
"""

import json, time, sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from scraper import search_google_maps

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
OUTPUT = DATA / "all_leads.json"

BRANCHEN = {
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

def load_existing():
    if OUTPUT.exists():
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    return []

def save_leads(leads):
    OUTPUT.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

def dedup_key(lead):
    return f"{lead.get('name','').lower().strip()}|{lead.get('address','').lower().strip()}"

def main():
    existing = load_existing()
    seen = {dedup_key(l) for l in existing}
    all_leads = list(existing)
    
    total_new = 0
    total_queries = 0
    errors = 0
    
    total_combos = sum(len(b) for _, b in BRANCHEN.items()) * len(STANDORTE)
    
    print(f"\n{'='*60}")
    print(f"  BATCH SCRAPE — TIER 3: Sonstige lokale Betriebe")
    print(f"  {total_combos} Queries ({sum(len(b) for _,b in BRANCHEN.items())} Branchen × {len(STANDORTE)} Städte)")
    print(f"  Bestehende Leads: {len(existing)}")
    print(f"  Start: {datetime.now():%H:%M:%S}")
    print(f"{'='*60}\n")
    
    for tier_name, branchen in BRANCHEN.items():
        print(f"\n--- {tier_name} ---")
        for branche in branchen:
            for stadt in STANDORTE:
                total_queries += 1
                query_label = f"[{total_queries}/{total_combos}] {branche} in {stadt}"
                
                try:
                    print(f"\n{query_label}")
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
                    print(f"  → {result.get('total_found', 0)} gefunden, {new_count} neu")
                    
                    if total_queries % 10 == 0:
                        save_leads(all_leads)
                        print(f"  💾 Zwischengespeichert: {len(all_leads)} Leads total")
                    
                    time.sleep(3 + (total_queries % 3))
                    
                except Exception as e:
                    errors += 1
                    print(f"  ❌ FEHLER: {e}")
                    time.sleep(5)
                    continue
    
    save_leads(all_leads)
    
    print(f"\n{'='*60}")
    print(f"  FERTIG — TIER 3")
    print(f"  Queries:     {total_queries}")
    print(f"  Neue Leads:  {total_new}")
    print(f"  Total Leads: {len(all_leads)}")
    print(f"  Fehler:      {errors}")
    print(f"  Ende:        {datetime.now():%H:%M:%S}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
