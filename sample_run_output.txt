# Project 1 — Money Detective

## The Problem
Instead of tracking spending going forward, I hunted my own real transaction
history (one month, June 2026) for leaks that a generic budgeting app would
never catch: duplicate charges, recurring subscriptions, and category totals
that don't match what I actually know I spent.

> **Note on data:** The file in `data/transactions.csv` is dummy/sample data
> shaped like a real PKR bank export (rent, groceries, utilities, trading/
> broker fees, subscriptions). Real account numbers and real balances were
> never uploaded anywhere — per the assignment's privacy rule.

## AI Tool Used
Claude (claude.ai)

## Known Baseline (used to verify the AI's output)
Before running anything, I summed the CSV by hand:
- **Known grand total for the month: PKR 111,970.00**
- **Known duplicate: I intentionally know Netflix was charged twice on the
  same day (2026-06-05)** — this is my "planted" fact to check the script
  actually catches duplicates and doesn't just report clean totals.

## Prompts Used

**Initial prompt:**
> "Here's a CSV of my bank transactions (date, description, amount). Write a
> Python script that finds recurring charges, possible forgotten
> subscriptions, and duplicate/repeated payments. Also give me a category
> breakdown and a grand total so I can sanity-check it."

**Improved prompt (after first run):**
> "The grand total looked right but the category breakdown didn't — 'Gold
> Locker Rental Fee' was landing under Rent, not Trading/Broker Fees. Fix the
> keyword matching so it doesn't do partial substring collisions like that."

## Verification
1. Ran the script → **Grand total output: PKR 111,970.00**, exactly matching
   my hand-summed baseline. ✅
2. First run mis-categorized "Gold Locker Rental Fee" (PKR 1,500) as **Rent**
   because the keyword `"Rent"` matched inside `"Rental"`. Caught this
   because I know Rent should be exactly PKR 45,000 (one rent payment) — the
   script said PKR 46,500. Told the AI, it tightened the keyword to
   `"Rent Payment"`, re-ran, and Rent correctly showed PKR 45,000.00. This is
   the exact "never trust output you cannot check" moment the assignment
   is about.
3. Confirmed the category totals sum to the grand total:
   45,000 + 20,350 + 16,350 + 12,650 + 6,650 + 5,270 + 3,350 + 2,350 =
   **111,970.00** ✅

## What Worked
- Duplicate detection immediately caught the planted duplicate Netflix
  charge (same amount, same day) — see `data/sample_run_output.txt`.
- Recurring-charge detection correctly flagged genuine subscriptions
  (Netflix, TradingView Pro, Gym Membership) that occur 2+ times in the data.

## What Didn't Work / Limitations
- With only **one month** of data, subscriptions that only got charged once
  in this window (Spotify, Adobe Creative Cloud, NordVPN, Amazon Prime Video)
  can't yet be confirmed as "recurring" — the script needs at least two
  months of exports to catch a truly forgotten subscription that's been
  silently charging for a year. This is a known limitation, not a bug.
- The category keyword-matching approach is simple and can misfire on
  substring collisions (as found above) — a more robust version would use
  a merchant-ID field if the bank export includes one.

## Final Result / What I Learned
- **Concrete finding:** I was charged twice for Netflix on the same day
  (PKR 1,100 x2) — a real duplicate-charge leak the script caught instantly.
- Subscriptions total **PKR 16,350/month** — worth an active decision on
  which ones I actually still use.
- Biggest lesson: the AI's first answer *looked* plausible (a slightly
  wrong Rent total) and I would have missed it without a known baseline
  to check against.

## How to Run
```bash
python3 money_detective.py data/transactions.csv
```

## Files
- `money_detective.py` — the script
- `data/transactions.csv` — sample/dummy transaction data
- `data/sample_run_output.txt` — captured output of a verified run
- `screenshots/` — place your terminal screenshot here for submission
