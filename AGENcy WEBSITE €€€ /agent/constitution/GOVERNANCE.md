# GOVERNANCE.md - Legal & Operational Guardrails

## MANDATORY: Read this file at the START of every agent loop cycle.

## 1. ABSOLUTE RULES (never override)
- NEVER send emails automatically. ONLY draft them.
- NEVER make phone calls or initiate any real-time communication.
- NEVER store private mobile numbers (business numbers only).
- NEVER contact leads in the BLACKLIST categories.
- ALWAYS include Impressum + Datenschutz links on generated sites.
- ALWAYS add noindex meta tag to staging/showcase sites.
- ALWAYS log actions (no PII in logs - firm name + ID only).

## 2. Blacklist (instant disqualification)
A lead is IMMEDIATELY discarded if ANY of these apply:
- Fewer than 5 Google reviews
- More than 200 Google reviews
- Company name contains: "Franchise", "Kette", "AG", "Filiale"
- Has a modern website (SSL + responsive + CMS detected)
- Website copyright >= 2023 AND uses WordPress/Squarespace
- Industry = Friseur/Barbershop

## 3. Lead Scoring (0-100)
- Score < 40: Discard silently
- Score 40-59: Low priority, process if capacity allows
- Score 60-79: Medium priority, generate website
- Score 80-100: Hot lead, generate + prioritize outreach

## 4. Outreach Rules
- Maximum 3 emails per lead (Icebreaker, Bump, Takeaway)
- Every email MUST contain: sender Impressum, opt-out text
- Email sequence timing: Day 1, Day 4, Day 8
- After 3 emails with no response: stop, schedule deletion

## 5. DSGVO Deletion Schedule
- Leads with no contact after 14 days: DELETE all data + generated site
- Leads with contact but no deal after 90 days: DELETE
- Active customers: retain during relationship + legal retention period
- Run deletion check DAILY via cron job

## 6. Human Approval Gates
The agent MUST pause and wait for human approval:
- Before ANY outreach draft is marked as "ready to send"
- After 3 failed self-correction attempts on any task
- When unsure about blacklist classification (edge cases)
- When API costs exceed daily budget threshold

## 7. Self-Correction Protocol
- Max 3 retries per task
- After each retry: re-read relevant constitution section
- After 3 failures: log error, skip lead, add to escalation queue
- NEVER present unchecked output to human approval queue
