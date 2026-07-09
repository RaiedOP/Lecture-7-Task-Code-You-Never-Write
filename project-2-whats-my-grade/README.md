# Project 2 — What's My Grade, Really

## The Problem
Generic grade-tracking apps don't know a specific teacher's actual rules:
weighted categories and a drop-lowest-quiz policy. I encoded my real
grading policy and had the AI calculate exactly where I stand — and what
I need on the final to hit my target.

> Scores in `data/scores.csv` are sample/dummy numbers (real course, made-up
> values) — structure and policy are real.

## AI Tool Used
Claude (claude.ai)

## The Policy (see `data/grading_policy.md` for full detail)
- Quizzes 15% (drop lowest quiz), Assignments 20%, Midterm 20%,
  Participation 10%, Final Exam 35%
- Target grade: 85%

## Prompts Used

**Initial prompt:**
> "Here are my scores by category and my teacher's exact grading policy
> (weights + a rule that drops my lowest quiz score). Write a Python script
> that calculates my current grade using these exact rules."

**Improved prompt (after first run):**
> "Now add a second calculation: given my current standing, what exact
> percentage do I need on the Final Exam (worth 35%) to reach an 85%
> target? Handle the edge cases — what if it's mathematically impossible,
> or if I've already secured it regardless of the final?"

## Verification (by hand)
I hand-calculated the **Quizzes** category myself:
- Raw: 8/10, 6/10, 9/10, 7/10, 10/10 → 80%, 60%, 90%, 70%, 100%
- Drop lowest (60%) → remaining: 80, 90, 70, 100 → average = **85.00%**
- Script output: `Quizzes avg 85.00% (lowest 1 dropped)` ✅ **Matches exactly.**

I also hand-checked the full weighted total (excluding the not-yet-taken
Final, which is 0):
`85×0.15 + 90×0.20 + 78×0.20 + 95×0.10 = 12.75 + 18.00 + 15.60 + 9.50 = 55.85`
→ Script output: **55.85%** ✅ Matches.

And the "score needed on final" math:
`(85 − 55.85) / 0.35 = 83.29%` → Script output: **83.29%** ✅ Matches.

## What Worked
- The drop-lowest-quiz logic works correctly (verified above).
- The "score needed on final" calculation handles the case where the
  final hasn't been taken yet (treated as 0% and backed out of the total).

## What Didn't Work / Problems Faced
- First draft of the AI's script applied the drop-lowest rule *after*
  weighting individual quizzes rather than *before* averaging the category
  — this would have silently given a wrong Quizzes percentage. Caught it by
  asking the AI to walk through the Quizzes math step by step against my
  hand calculation, and it corrected the order of operations.

## Final Result / What I Learned
- **Current true grade: 55.85%** (Final Exam not yet taken, correctly
  scored as an open weight rather than a zero-dragging-everything-down
  number for categories already complete).
- **I need 83.29% on the Final Exam** to hit my 85% target.
- Lesson: weighted-average grade math has a lot of silent ordering bugs
  (drop-before-weight vs. weight-before-drop) — verifying one category by
  hand caught a real error.

## How to Run
```bash
python3 grade_calculator.py data/scores.csv
```

## Files
- `grade_calculator.py` — the script
- `data/scores.csv` — sample scores
- `data/grading_policy.md` — the teacher's rules, written out
- `data/sample_run_output.txt` — captured output of a verified run
- `screenshots/` — place your terminal screenshot here for submission
