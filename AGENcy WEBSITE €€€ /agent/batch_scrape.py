#!/usr/bin/env python3
"""
Batch-Scraper: Berlin + Brandenburg, alle Zielbranchen.
Speichert in data/all_leads.json (append, dedupliziert nach Name+Adresse).
"""

import json, time, sys, os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from scraper import search_google_maps

DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
OUTPUT = DATA / "all_leads.json"

# ══════════════════════════════════════════════════════════════
#  Zielbranchen
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
}

# ══════════════════════════════════════════════════════════════
#  Standorte: Berlin + Brandenburg
# ══════════════════════════════════════════════════════════════

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
#  Scraping
# ══════════════════════════════════════════════════════════════

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
    
    # Optionale Filter
    only_tier = sys.argv[1] if len(sys.argv) > 1 else None
    only_city = sys.argv[2] if len(sys.argv) > 2 else None
    
    tiers = BRANCHEN.items()
    if only_tier:
        tiers = [(k, v) for k, v in tiers if only_tier.lower() in k.lower()]
    
    standorte = STANDORTE
    if only_city:
        standorte = [s for s in standorte if only_city.lower() in s.lower()]
    
    total_combos = sum(len(branchen) for _, branchen in tiers) * len(standorte)
    
    print(f"\n{'='*60}")
    print(f"  BATCH SCRAPE")
    print(f"  {total_combos} Queries ({sum(len(b) for _,b in tiers)} Branchen × {len(standorte)} Städte)")
    print(f"  Bestehende Leads: {len(existing)}")
    print(f"  Start: {datetime.now():%H:%M:%S}")
    print(f"{'='*60}\n")
    
    for tier_name, branchen in tiers:
        print(f"\n--- {tier_name} ---")
        for branche in branchen:
            for stadt in standorte:
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
                    
                    # Zwischenspeichern alle 10 Queries
                    if total_queries % 10 == 0:
                        save_leads(all_leads)
                        print(f"  💾 Zwischengespeichert: {len(all_leads)} Leads total")
                    
                    # Rate limiting: 3-5s zwischen Queries
                    time.sleep(3 + (total_queries % 3))
                    
                except Exception as e:
                    errors += 1
                    print(f"  ❌ FEHLER: {e}")
                    time.sleep(5)
                    continue
    
    # Final speichern
    save_leads(all_leads)
    
    # Stats
    print(f"\n{'='*60}")
    print(f"  FERTIG")
    print(f"  Queries:     {total_queries}")
    print(f"  Neue Leads:  {total_new}")
    print(f"  Total Leads: {len(all_leads)}")
    print(f"  Fehler:      {errors}")
    print(f"  Ende:        {datetime.now():%H:%M:%S}")
    print(f"{'='*60}\n")
    
    # Quick stats nach Tier
    for tier_name in BRANCHEN:
        tier_leads = [l for l in all_leads if l.get("tier") == tier_name]
        no_web = len([l for l in tier_leads if not l.get("website")])
        print(f"  {tier_name}: {len(tier_leads)} Leads ({no_web} ohne Website)")


if __name__ == "__main__":
    main()
