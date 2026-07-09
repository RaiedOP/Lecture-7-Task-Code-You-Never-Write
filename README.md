"""
Money Detective
----------------
Hunts for leaks hiding in real transaction history:
  - Duplicate/repeated charges (same description + amount within a short window)
  - Recurring charges (appear 2+ times across the month -> likely subscriptions)
  - A simple category breakdown + grand total, so it can be checked against a
    known baseline figure by hand.

Usage:
    python money_detective.py data/transactions.csv

Everything below is deliberately readable in plain English (see README.md
for the "explain this to me" pass this script went through).
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime

DUPLICATE_WINDOW_DAYS = 3  # same charge within this many days = likely duplicate


def load_transactions(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "date": datetime.strptime(row["date"], "%Y-%m-%d"),
                "description": row["description"].strip(),
                "amount": float(row["amount"]),
            })
    return rows


def find_duplicates(transactions):
    """Same description + same amount, within DUPLICATE_WINDOW_DAYS of each other."""
    by_key = defaultdict(list)
    for t in transactions:
        by_key[(t["description"], t["amount"])].append(t)

    duplicates = []
    for (desc, amount), txns in by_key.items():
        txns.sort(key=lambda t: t["date"])
        for i in range(1, len(txns)):
            gap = (txns[i]["date"] - txns[i - 1]["date"]).days
            if gap <= DUPLICATE_WINDOW_DAYS:
                duplicates.append({
                    "description": desc,
                    "amount": amount,
                    "date_1": txns[i - 1]["date"].date(),
                    "date_2": txns[i]["date"].date(),
                    "gap_days": gap,
                })
    return duplicates


def find_recurring(transactions):
    """Descriptions that show up 2+ times across the month -> likely subscriptions."""
    counts = defaultdict(list)
    for t in transactions:
        counts[t["description"]].append(t["amount"])

    recurring = []
    for desc, amounts in counts.items():
        if len(amounts) >= 2:
            recurring.append({
                "description": desc,
                "occurrences": len(amounts),
                "total_spent": round(sum(amounts), 2),
                "avg_amount": round(sum(amounts) / len(amounts), 2),
            })
    recurring.sort(key=lambda r: -r["total_spent"])
    return recurring


def category_breakdown(transactions):
    """Very rough keyword-based categorization for a quick sanity check."""
    categories = {
        "Rent": ["Rent Payment"],
        "Groceries": ["Grocery"],
        "Utilities": ["Electricity", "K-Electric", "Internet", "PTCL", "Mobile Load"],
        "Subscriptions": ["Subscription", "Netflix", "Spotify", "Adobe", "VPN",
                           "Prime Video", "TradingView"],
        "Transport": ["Careem"],
        "Food Delivery": ["Foodpanda"],
        "Trading/Broker Fees": ["Broker", "Gold Locker"],
        "Other": [],
    }
    totals = defaultdict(float)
    for t in transactions:
        matched = "Other"
        for cat, keywords in categories.items():
            if any(k.lower() in t["description"].lower() for k in keywords):
                matched = cat
                break
        totals[matched] += t["amount"]
    return {k: round(v, 2) for k, v in totals.items() if v > 0}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/transactions.csv"
    transactions = load_transactions(path)

    grand_total = round(sum(t["amount"] for t in transactions), 2)

    print("=" * 60)
    print("MONEY DETECTIVE — REPORT")
    print("=" * 60)

    print(f"\nTotal transactions analyzed: {len(transactions)}")
    print(f"GRAND TOTAL SPENT (this period): PKR {grand_total:,.2f}")
    print("  -> Compare this number to your known baseline (e.g. your bank")
    print("     statement's closing total spend) before trusting anything below.")

    print("\n--- Category Breakdown ---")
    for cat, total in sorted(category_breakdown(transactions).items(), key=lambda x: -x[1]):
        print(f"  {cat:<20} PKR {total:,.2f}")

    print("\n--- Possible Duplicate / Repeated Charges (within "
          f"{DUPLICATE_WINDOW_DAYS} days) ---")
    dups = find_duplicates(transactions)
    if dups:
        for d in dups:
            print(f"  ⚠ '{d['description']}' charged PKR {d['amount']:,.2f} twice: "
                  f"{d['date_1']} and {d['date_2']} ({d['gap_days']} day(s) apart)")
    else:
        print("  None found.")

    print("\n--- Recurring Charges (possible subscriptions) ---")
    for r in find_recurring(transactions):
        print(f"  {r['description']:<30} x{r['occurrences']}  "
              f"total PKR {r['total_spent']:,.2f}  (avg PKR {r['avg_amount']:,.2f})")

    print("\n--- Flag: Subscriptions worth double-checking ---")
    print("  (Recurring AND small/easy-to-forget: Spotify, Adobe, VPN, Prime Video)")
    watch_list = ["Spotify", "Adobe", "VPN", "Prime Video"]
    for r in find_recurring(transactions):
        if any(w.lower() in r["description"].lower() for w in watch_list):
            print(f"  🔎 {r['description']} — do you still use this?")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
