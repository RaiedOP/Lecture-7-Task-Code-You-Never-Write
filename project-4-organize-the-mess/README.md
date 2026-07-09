# Project 4 — Organize the Mess (The Files You Forgot)

## The Problem
A messy folder (Downloads + Documents + Screenshots) accumulates duplicate
files under different names, forgotten screenshots, and drafts. This
project is different from the other three: it touches real files, so it
follows a strict safety order.

> `sample_messy_folder/` is a synthetic stand-in folder with placeholder
> file contents (not real personal files) so the duplicate-detection logic
> can be demonstrated safely and reproducibly.

## AI Tool Used
Claude (claude.ai)

## The Brief ("clean" means, in plain language)
- Find **true duplicates** — same content, even if the filename is
  different (e.g. `report_final.docx` vs `report_final_v2.docx` vs
  `report_final(1).docx` — all three turned out to be byte-for-byte
  identical).
- Flag large files.
- Group everything else by type (Documents / Images / Videos / Other).
- **Never touch the originals** — only ever copy into a new `organized/`
  folder.

## Prompts Used

**Initial prompt:**
> "I have a messy Downloads/Documents/Screenshots folder with duplicate
> files saved under different names, plus random screenshots. Write a
> Python script that finds true duplicates by file content (not just
> filename), flags large files, and groups the rest by type."

**Improved / safety-focused prompt:**
> "Before this touches any real files: show me the full plan first — every
> file you'd copy, skip, or flag — and don't move or delete anything unless
> I explicitly pass an `--execute` flag. Even then, only copy into a new
> `organized/` folder; never overwrite or delete anything in the original
> folder."

## Safety Order Followed
1. **Copy first** — this script is read-only against the source folder by
   design; it never opens the source in write mode.
2. **Wrote the brief** (above) before any code was generated.
3. **Demanded a dry run** — default behavior (no `--execute` flag) only
   prints the plan. See `data/dry_run_output.txt`.
4. **Reviewed the plan** — checked every proposed COPY and DUPLICATE line
   against what I expected before approving.
5. **Approved and executed** — only after review did I run
   `python3 organize.py sample_messy_folder --execute`. See
   `data/execute_output.txt`.
6. **Verified** — confirmed the **original** `sample_messy_folder/` still
   has all 13 files, untouched, and the new `organized/` folder (saved here
   as `data/organized_output_example/`) has the de-duplicated, type-sorted
   copies.

## Verification
- Known fact going in: I know `report_final.docx`,
  `report_final_v2.docx`, and `report_final(1).docx` are the exact same
  file saved three times under different names. The dry run correctly
  flagged 2 of the 3 as duplicates of the third, by content hash — not by
  matching the filename (which wouldn't have caught this).
- Known fact: `invoice_2026_06.pdf` and `invoice_2026_06 (copy).pdf` are
  identical → correctly flagged.
- Ran `find sample_messy_folder -type f` **before and after** execution —
  identical 13-file list both times, confirming originals were never
  moved, renamed, or deleted. ✅

## What Worked
- Content-hash duplicate detection catches renamed duplicates that a
  filename-only check would completely miss.
- The dry-run/execute split meant I could review the exact plan
  (down to individual COPY lines) with zero risk before anything ran.

## What Didn't Work / Problems Faced
- First draft of the script deleted originals after copying (a "move"
  instead of a "copy"). I caught this by reading the plan output closely —
  it said "moved" instead of "copied." Explicitly told the AI: copy only,
  never move or delete, and re-verified with the before/after file listing
  above.
- Large-file flagging is currently trivial in this demo (a placeholder
  threshold of 0 bytes, since the sample files are tiny). For a real
  Downloads folder, set `LARGE_FILE_THRESHOLD_BYTES` to something real,
  e.g. `100_000_000` (100MB).

## Final Result / What I Learned
- Found **5 duplicate files** across 3 duplicate "families," reclaiming
  the wasted copies without touching a single original.
- Lesson: for any script that touches real files, "show me the plan,
  wait for approval" isn't optional — the first draft's silent switch from
  copy to move is exactly the kind of thing that could quietly delete
  something important if I hadn't demanded a dry run first.

## How to Run
```bash
# 1. Dry run (safe, default) — review the plan first
python3 organize.py sample_messy_folder

# 2. Only after reviewing the plan, execute it
python3 organize.py sample_messy_folder --execute
```

## Files
- `organize.py` — the script
- `sample_messy_folder/` — synthetic messy folder used for this demo
- `data/dry_run_output.txt` — captured dry-run plan
- `data/execute_output.txt` — captured execution log
- `data/organized_output_example/` — the resulting organized copy
- `screenshots/` — place your terminal screenshot here for submission
