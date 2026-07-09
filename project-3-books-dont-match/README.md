# Project 3 — The Books Don't Match

## The Problem
A group trip fund was hand-counted at a known total. The digital payment
record (bank transfer history) that's supposed to represent the same
collections has inconsistent names, partial payments, and at least one
totally unidentified sender. I reconciled the two and named exactly who
still needs to pay.

> `data/digital_payments.csv` is dummy/sample data. Names, phone-style
> memos, and amounts are made up — the ambiguity pattern is real.

## AI Tool Used
Claude (claude.ai)

## Known Total (stated up front, before looking at the records)
**PKR 40,000** — 8 members × PKR 5,000 each, hand-counted.

## Prompts Used

**Initial prompt:**
> "I collected PKR 40,000 in cash from 8 people for a trip (5,000 each).
> Here's the messy digital transfer record that's supposed to match —
> inconsistent names, some partial payments, some I can't identify. Here
> are my own rules for who's who (attached). Write a script that resolves
> names using these exact rules, then tells me the gap and exactly who
> still needs to pay."

**Improved prompt (after first run):**
> "One entry says 'Hassan — already paid part, PKR 2,000' — that's actually
> an unrelated rent split between Hassan and his roommate, not trip money.
> Add a rule to exclude any 'already paid part' memo from Hassan
> specifically, and show excluded entries separately so I can see what was
> filtered out and why."

## Verification
By hand, I traced 3 people's entries against my own memory of who sent what:
- **Sara**: `Sara K` (2,500) + `S.K.` (2,500) = **5,000** ✅ matches what
  I remember her confirming in the group chat.
- **Bilal**: `Bilal` (5,000) + `BILAL AHMED` (2,500) = **7,500** — I know
  he accidentally sent extra, matching the script's "overpaid" flag. ✅
- **Ahmed vs. Bilal name collision**: I specifically checked that `"BILAL
  AHMED"` didn't get swept into Ahmed's total just because it contains
  "Ahmed" — confirmed the script correctly routes it to Bilal (his full
  name), because my rule for that specific string is more specific than
  the generic Ahmed rule.

Matched total (32,500) + gap (7,500) = 40,000 → arithmetic checks out
against the known total. ✅

## What Worked
- Excluding the unrelated Hassan entry instead of blindly counting it
  prevented a false "he overpaid" result.
- Clearly separating "excluded" vs. "unmatched/unknown" vs. "resolved"
  entries made the gap explainable instead of just a single scary number.

## What Didn't Work / Problems Faced
- The script can't resolve the `"unknown"` sender on its own — and it
  shouldn't try to. First AI draft guessed it was probably Usman based on
  timing; I rejected that and told it explicitly: never guess an identity,
  just flag it for a human to confirm.

## Final Result / What I Learned
- **PKR 7,500 is still unaccounted for.**
- **Usman and Fatima have no recorded payment** — direct follow-up needed.
- **Bilal overpaid by PKR 2,500** — likely covers part of the gap once
  confirmed, or needs a refund.
- One **unidentified PKR 5,000 "cash deposit"** could belong to Usman or
  Fatima — needs a direct question, not a guess.
- Lesson: the AI is good at doing the arithmetic once the identity rules
  are spelled out — but the identity rules themselves have to come from me,
  not the AI, because only I know who "S.K." or "unknown" actually is.

## How to Run
```bash
python3 reconcile.py data/digital_payments.csv
```

## Files
- `reconcile.py` — the script
- `data/digital_payments.csv` — sample/dummy messy payment record
- `data/reconciliation_rules.md` — my personal name-resolution rules + known total
- `data/sample_run_output.txt` — captured output of a verified run
- `screenshots/` — place your terminal screenshot here for submission
