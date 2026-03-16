#!/bin/bash
# Auto-restart wrapper für batch_scrape_all.py
# Startet den Scraper immer wieder neu bis alle Queries fertig sind.

cd "$(dirname "$0")"
LOG="logs/scraper_$(date +%Y%m%d).log"

echo "=== Scraper Auto-Restart gestartet $(date) ===" | tee -a "$LOG"

while true; do
    echo "" | tee -a "$LOG"
    echo "--- Starte Scraper $(date +%H:%M:%S) ---" | tee -a "$LOG"
    
    python3 batch_scrape_all.py 2>&1 | tee -a "$LOG"
    EXIT_CODE=$?
    
    # Check ob alle Queries fertig (Script gibt "Noch zu scrapen: 0" aus)
    REMAINING=$(python3 -c "
import json
from pathlib import Path
from batch_scrape_all import BRANCHEN, STANDORTE, get_done_combos, load_existing
existing = load_existing()
done = get_done_combos(existing)
total = sum(len(b) for b in BRANCHEN.values()) * len(STANDORTE)
todo = total - len(done)
print(todo)
" 2>/dev/null)
    
    echo "  Exit code: $EXIT_CODE | Remaining: $REMAINING" | tee -a "$LOG"
    
    if [ "$REMAINING" = "0" ] 2>/dev/null; then
        echo "=== ALLE QUERIES FERTIG $(date) ===" | tee -a "$LOG"
        # Final stats
        python3 -c "
import json
with open('data/all_leads.json') as f:
    data = json.load(f)
new = [l for l in data if l.get('tier')]
print(f'FINAL: {len(data)} Leads total, {len(new)} neu')
for t in sorted(set(l.get('tier','') for l in new)):
    if t:
        tl = [l for l in new if l.get('tier')==t]
        nw = len([l for l in tl if not l.get('website')])
        print(f'  {t}: {len(tl)} ({nw} ohne Website)')
print(f'  Ohne Website gesamt: {len([l for l in data if not l.get(\"website\")])}')
" 2>&1 | tee -a "$LOG"
        break
    fi
    
    echo "  Warte 15s vor Neustart..." | tee -a "$LOG"
    sleep 15
done

echo "=== Scraper beendet $(date) ===" | tee -a "$LOG"
