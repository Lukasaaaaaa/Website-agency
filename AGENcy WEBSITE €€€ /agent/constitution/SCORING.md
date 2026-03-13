# SCORING.md - Lead Qualification Rules

## Scoring Formula

### Disqualifiers (score = 0, discard immediately)
- reviews < 5
- reviews > 200
- name contains franchise/kette/ag/filiale
- has modern website (ssl + responsive + recent cms)
- industry in [friseur, barbershop]

### Positive Signals
| Signal                              | Points |
|-------------------------------------|--------|
| 15-100 Google reviews               | +30    |
| 5-14 Google reviews                 | +10    |
| No website / returns 404            | +25    |
| Website exists but not responsive   | +20    |
| Owner uploads photos (last 6 months)| +15    |
| Reviews are answered                | +10    |
| GmbH or GmbH & Co. KG              | +10    |
| Rating >= 4.0 stars                 | +5     |
| Niche = Handwerker                  | +10    |
| Niche = Physio                      | +8     |
| Niche = GaLaBau                     | +6     |
| Niche = Fahrschule                  | +4     |

### Score Interpretation
| Score | Action                                        |
|-------|-----------------------------------------------|
| 0     | Blacklisted, discard                          |
| 1-39  | Too low potential, discard                    |
| 40-59 | Low priority, process if queue is empty       |
| 60-79 | Medium priority, generate website             |
| 80-100| Hot lead, generate + rush to approval queue   |
