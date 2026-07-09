# Lecture 7 Report — Code You Never Write

**Student:** RaiedOP (Raied)
**Program:** Panaversity AI-101 Agentic AI Architect Program

## Overview
Across all four projects, I acted as the client: I described each problem
in plain language, handed it to Claude, and checked every output against a
fact I already knew was true before trusting the rest. This report covers
what I asked for, how I verified it, what went wrong, and what I learned —
for each of the four projects.

---

## Project 1 — Money Detective

**Problem:** Find spending leaks in a month of real transaction history
that a generic budgeting app would never catch.

**AI tool used:** Claude

**Initial prompt:** Paste a CSV of transactions (date, description, amount)
and ask for a script that finds recurring charges, forgotten subscriptions,
and duplicate payments, plus a category breakdown and grand total.

**Improved prompt:** After the first run mis-sorted "Gold Locker Rental
Fee" into the Rent category (because the keyword `"Rent"` matched inside
`"Rental"`), asked the AI to fix the keyword matching so it can't collide
like that.

**Verification:** Hand-summed the CSV to get a known grand total of
PKR 111,970.00 — the script matched exactly. Also knew Rent should be
exactly PKR 45,000 (a single payment); the buggy first run said
PKR 46,500, which is what caught the keyword bug.

**What worked:** Duplicate detection instantly caught a Netflix charge
that was billed twice on the same day. Recurring-charge detection
correctly identified genuine subscriptions.

**What didn't work:** With only one month of data, subscriptions charged
just once in that window (Spotify, Adobe, NordVPN) can't yet be confirmed
as forgotten — that check needs multiple months of history.

**Final result:** Found a real duplicate charge (PKR 1,100 x2) and a clear
view of PKR 16,350/month going to subscriptions.

---

## Project 2 — What's My Grade, Really

**Problem:** School grade apps don't know a specific teacher's real rules
(weighted categories, drop-lowest-quiz). Encoded the exact policy to find
my true current standing.

**AI tool used:** Claude

**Initial prompt:** Provide real scores by category and the teacher's exact
weights + drop rule, and ask for a script that calculates the current
grade using those exact rules.

**Improved prompt:** Asked for a second calculation — the exact Final Exam
score needed to hit an 85% target, including edge cases (impossible target,
already-secured target).

**Verification:** Hand-calculated the Quizzes category myself (drop the
lowest of 5 quiz scores, then average the rest) and got 85.00% — matched
the script exactly. Also hand-checked the full weighted total (55.85%) and
the final-exam score needed (83.29%) — both matched.

**What worked:** The drop-lowest-quiz logic and the "score needed" backward
calculation both checked out against hand math.

**What didn't work:** The first draft applied the drop-lowest rule in the
wrong order (after weighting individual quizzes instead of before
averaging the category), which would have silently produced a wrong
percentage. Caught by walking through the Quizzes math step by step.

**Final result:** True current grade of 55.85% (Final Exam not yet taken),
needing 83.29% on the final to reach an 85% target.

---

## Project 3 — The Books Don't Match

**Problem:** Reconcile a hand-counted group trip fund total against a
messy digital transfer record with inconsistent, ambiguous sender names.

**AI tool used:** Claude

**Initial prompt:** State the known hand-counted total (PKR 40,000 from 8
people), provide the raw messy transfer record, provide personal
name-resolution rules, and ask for a script that resolves names using
those exact rules and reports the gap plus who still needs to pay.

**Improved prompt:** Flagged that one entry ("Hassan — already paid part,
PKR 2,000") was actually an unrelated rent split with a roommate, not trip
money — asked the AI to exclude it via a specific rule rather than
counting it toward Hassan's trip total.

**Verification:** Hand-traced Sara's two partial payments (2,500 + 2,500 =
5,000) and Bilal's payment plus his "BILAL AHMED" entry (5,000 + 2,500 =
7,500, an overpayment) against my own memory of the group chat. Confirmed
the script routes "BILAL AHMED" to Bilal and not to "Ahmed," despite the
substring match. Matched total (32,500) + gap (7,500) = known total
(40,000) — arithmetic checks out.

**What worked:** Explicitly separating "excluded" vs. "unmatched/unknown"
vs. "resolved" entries made a scary single gap number explainable.

**What didn't work:** The first draft guessed that the unidentified
"unknown / cash deposit" sender was probably one of the missing people
based on timing. Rejected that — the AI shouldn't guess an identity, only
flag it for a human to confirm.

**Final result:** PKR 7,500 unaccounted for. Two people (out of 8) have no
recorded payment and need direct follow-up; one overpayment and one
unidentified deposit still need confirming.

---

## Project 4 — Organize the Mess

**Problem:** A messy Downloads/Documents/Screenshots folder has duplicate
files saved under different names, forgotten screenshots, and clutter.
Unlike the first three, this one touches real files, so it required a
strict safety discipline.

**AI tool used:** Claude

**Initial prompt:** Describe the messy folder and ask for a script that
finds true duplicates by file content (not just filename), flags large
files, and groups the rest by type.

**Safety-focused prompt:** Required the AI to show the full plan first —
every file it would copy, skip, or flag — and to never move, rename, or
delete anything unless an explicit `--execute` flag was passed, and even
then to only copy into a new `organized/` folder, never touching the
originals.

**Verification:** Ran a dry run first and reviewed every line. Confirmed
by content-hash that three differently-named files
(`report_final.docx`, `report_final_v2.docx`, `report_final(1).docx`) were
byte-for-byte identical, and two invoices were identical despite one being
named "(copy)". After execution, compared a full file listing of the
original folder before and after — identical 13 files both times, proving
nothing was moved or deleted.

**What worked:** Content-hash duplicate detection caught renamed
duplicates that filename matching alone would have missed completely.

**What didn't work:** The first draft of the script actually *moved* files
into the organized folder instead of copying them, which would have
deleted originals from their source location. Caught this by reading the
dry-run plan closely (it said "moved," not "copied") before ever running
`--execute`. Explicitly corrected the AI to copy-only.

**Final result:** Found 5 duplicate files across 3 duplicate "families,"
reclaimed the wasted copies, and organized the rest by type — with zero
risk to the originals, verified with a before/after file listing.

---

## Overall Reflection
The pattern across all four projects was the same: the AI's first answer
almost always *looked* correct, and in three of the four projects it
contained a real, specific error that only surfaced because I checked it
against something I already knew — a known total, a known category value,
a known duplicate, or a known safety requirement (copy vs. move). The
"client, not coder" model works specifically because verification against
a known fact is cheap and catches errors that reading the code line-by-line
might not.
