"""
What's My Grade, Really
------------------------
Encodes one specific teacher's grading policy (weights per category,
drop-lowest-quiz rule) and calculates the true current grade, plus the
exact final-exam score needed to hit a target grade.

Usage:
    python grade_calculator.py data/scores.csv
"""

import csv
import sys
from collections import defaultdict

# --- Teacher's actual policy (see data/grading_policy.md) ---
WEIGHTS = {
    "Quizzes": 0.15,
    "Assignments": 0.20,
    "Midterm": 0.20,
    "Participation": 0.10,
    "Final": 0.35,
}
DROP_LOWEST = {"Quizzes": 1}  # drop the lowest N scores in this category
TARGET_GRADE = 85.0  # percent


def load_scores(path):
    by_category = defaultdict(list)
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            by_category[row["category"]].append({
                "item": row["item"],
                "score": float(row["score"]),
                "max_score": float(row["max_score"]),
            })
    return by_category


def category_percentage(category, items):
    """Convert each item to a percentage, apply drop-lowest rule, then average."""
    percentages = [(i["score"] / i["max_score"]) * 100 for i in items]
    drop_n = DROP_LOWEST.get(category, 0)
    if drop_n and len(percentages) > drop_n:
        percentages = sorted(percentages)[drop_n:]  # drop the lowest N
    return sum(percentages) / len(percentages)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/scores.csv"
    by_category = load_scores(path)

    print("=" * 60)
    print("WHAT'S MY GRADE, REALLY — REPORT")
    print("=" * 60)

    weighted_total = 0.0
    category_results = {}

    for category, weight in WEIGHTS.items():
        items = by_category.get(category, [])
        if not items:
            continue
        pct = category_percentage(category, items)
        category_results[category] = pct
        contribution = pct * weight
        weighted_total += contribution
        drop_note = ""
        if category in DROP_LOWEST:
            drop_note = f" (lowest {DROP_LOWEST[category]} dropped)"
        print(f"  {category:<14} avg {pct:6.2f}%  x weight {weight:.0%}  "
              f"= {contribution:5.2f} pts{drop_note}")

    print(f"\nCURRENT GRADE (as it stands right now): {weighted_total:.2f}%")

    # --- What score do I need on the final to hit the target? ---
    final_weight = WEIGHTS["Final"]
    grade_without_final = weighted_total - (category_results.get("Final", 0) * final_weight)
    needed_final_pct = (TARGET_GRADE - grade_without_final) / final_weight

    print(f"\nTarget grade: {TARGET_GRADE:.1f}%")
    if needed_final_pct > 100:
        print(f"  ⚠ You would need {needed_final_pct:.2f}% on the final — "
              f"mathematically impossible. Target may be out of reach for this term.")
    elif needed_final_pct < 0:
        print(f"  ✅ You've already secured the target grade regardless of "
              f"the final exam (needed: {needed_final_pct:.2f}%).")
    else:
        print(f"  ➤ You need at least {needed_final_pct:.2f}% on the Final Exam "
              f"to reach {TARGET_GRADE:.1f}%.")

    print("=" * 60)


if __name__ == "__main__":
    main()
