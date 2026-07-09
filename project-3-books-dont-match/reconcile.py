"""
The Books Don't Match
-----------------------
Reconciles a known, hand-counted total against a messy digital payment
record with inconsistent/ambiguous sender names — using personal
knowledge-based rules (see data/reconciliation_rules.md) to resolve who's
who, rather than guessing.

Usage:
    python reconcile.py data/digital_payments.csv
"""

import csv
import sys
from collections import defaultdict

KNOWN_TOTAL = 40000  # hand-counted, told to the script up front
EXPECTED_PER_PERSON = 5000
EXPECTED_MEMBERS = ["Ahmed", "Sara", "Bilal", "Hassan", "Zainab", "Ayesha",
                    "Usman", "Fatima"]


def resolve_name(raw_name, memo):
    """Personal rules for interpreting ambiguous entries — see
    data/reconciliation_rules.md. Returns a resolved name, or None if the
    entry must be excluded, or 'UNKNOWN' if it can't be assigned at all.
    """
    name = raw_name.strip()
    memo = (memo or "").strip().lower()

    if name.lower() == "unknown":
        return "UNKNOWN"

    if "bilal ahmed" in name.lower():
        return "Bilal"
    if "ahmed" in name.lower():
        return "Ahmed"
    if name.lower() in ("sara k", "s.k."):
        return "Sara"
    if "bilal" in name.lower():
        return "Bilal"
    if "hassan" in name.lower():
        if memo == "already paid part":
            # Personal knowledge: this is an unrelated rent-split, not trip dues.
            return None
        return "Hassan"
    if "zainab" in name.lower():
        return "Zainab"
    if "ayesha" in name.lower():
        return "Ayesha"

    return "UNKNOWN"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/digital_payments.csv"

    resolved_totals = defaultdict(float)
    unknown_entries = []
    excluded_entries = []
    raw_total = 0.0

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row["amount"])
            raw_total += amount
            resolved = resolve_name(row["sender_name_raw"], row["memo"])
            if resolved is None:
                excluded_entries.append(row)
                continue
            if resolved == "UNKNOWN":
                unknown_entries.append(row)
                continue
            resolved_totals[resolved] += amount

    print("=" * 60)
    print("THE BOOKS DON'T MATCH — RECONCILIATION REPORT")
    print("=" * 60)

    print(f"\nKnown hand-counted total (the target):  PKR {KNOWN_TOTAL:,.2f}")
    print(f"Raw sum of ALL digital entries (before any rules): PKR {raw_total:,.2f}")

    print("\n--- Per-Person Resolved Totals ---")
    for member in EXPECTED_MEMBERS:
        total = resolved_totals.get(member, 0.0)
        status = ""
        if total == 0:
            status = "  ⚠ HAS NOT PAID"
        elif total < EXPECTED_PER_PERSON:
            status = f"  ⚠ SHORT by PKR {EXPECTED_PER_PERSON - total:,.2f}"
        elif total > EXPECTED_PER_PERSON:
            status = f"  ⚠ OVERPAID by PKR {total - EXPECTED_PER_PERSON:,.2f}"
        else:
            status = "  ✅ fully paid"
        print(f"  {member:<10} PKR {total:>9,.2f}{status}")

    matched_total = sum(resolved_totals.values())

    print("\n--- Excluded Entries (personal-knowledge rule applied) ---")
    for e in excluded_entries:
        print(f"  Excluded: {e['date']} '{e['sender_name_raw']}' "
              f"PKR {float(e['amount']):,.2f} — memo: '{e['memo']}' "
              f"(unrelated to trip dues)")

    print("\n--- Unmatched Entries (need follow-up — do NOT guess) ---")
    unknown_total = 0.0
    for e in unknown_entries:
        unknown_total += float(e["amount"])
        print(f"  ❓ {e['date']} sender='{e['sender_name_raw']}' "
              f"PKR {float(e['amount']):,.2f} memo: '{e['memo']}'")

    gap = KNOWN_TOTAL - matched_total
    print(f"\nMatched total (resolved to a named person): PKR {matched_total:,.2f}")
    print(f"Unmatched (unknown sender) total: PKR {unknown_total:,.2f}")
    print(f"\nGAP vs. known hand-counted total: PKR {gap:,.2f} still unaccounted for")

    missing_people = [m for m in EXPECTED_MEMBERS if resolved_totals.get(m, 0) == 0]
    print(f"\nFollow up with: {', '.join(missing_people)} "
          f"(no payment recorded under their name)")
    print("Also confirm who the 'unknown / cash deposit' entry belongs to — "
          "it may cover one of the people above.")

    print("=" * 60)


if __name__ == "__main__":
    main()
