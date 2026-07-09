"""
Organize the Mess (The Files You Forgot)
------------------------------------------
Finds duplicates (by content hash, not just filename), flags large files,
and groups files by type — but NEVER touches originals directly.

Safety order (per assignment instructions):
  1. Copy first — this script only ever reads from the source folder.
  2. Write the brief — see PROMPTS.md for what "clean" means here.
  3. Dry run — running with no flags ONLY prints the plan. Nothing moves.
  4. Review — read the printed plan.
  5. Approve & execute — only `--execute` actually writes files, and it
     writes to a NEW `organized/` folder, never overwriting the source.
  6. Verify — spot-check the organized folder afterward.

Usage:
    python organize.py sample_messy_folder                 # dry run (default, safe)
    python organize.py sample_messy_folder --execute        # actually organizes (into organized/)
"""

import hashlib
import os
import shutil
import sys
from collections import defaultdict

LARGE_FILE_THRESHOLD_BYTES = 0  # for this demo, any placeholder counts; set a
                                  # real threshold (e.g. 100_000_000 for 100MB) for real folders

TYPE_FOLDERS = {
    ".png": "Images", ".jpg": "Images", ".jpeg": "Images",
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".mp4": "Videos", ".mov": "Videos",
}


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def scan_folder(source):
    files = []
    for root, _, filenames in os.walk(source):
        for name in filenames:
            full_path = os.path.join(root, name)
            files.append(full_path)
    return files


def build_plan(source):
    files = scan_folder(source)
    by_hash = defaultdict(list)
    for f in files:
        by_hash[file_hash(f)].append(f)

    duplicates = []
    keep_files = []
    for h, paths in by_hash.items():
        paths.sort()
        keep_files.append(paths[0])
        for extra in paths[1:]:
            duplicates.append({"keep": paths[0], "duplicate": extra})

    large_files = []
    for f in files:
        size = os.path.getsize(f)
        if size > LARGE_FILE_THRESHOLD_BYTES:
            large_files.append({"path": f, "size_bytes": size})

    # group non-duplicate files by type for the organized copy
    grouped = defaultdict(list)
    for f in keep_files:
        ext = os.path.splitext(f)[1].lower()
        folder = TYPE_FOLDERS.get(ext, "Other")
        grouped[folder].append(f)

    return {"duplicates": duplicates, "large_files": large_files, "grouped": grouped}


def print_plan(plan, dest):
    print("=" * 60)
    print("ORGANIZE THE MESS — PROPOSED PLAN (nothing has moved yet)")
    print("=" * 60)

    print(f"\nDestination for organized copy: {dest}/  (originals untouched)")

    print(f"\n--- Duplicate files found ({len(plan['duplicates'])}) ---")
    for d in plan["duplicates"]:
        print(f"  DUPLICATE: '{d['duplicate']}'")
        print(f"    -> same content as: '{d['keep']}'")
        print(f"    -> proposed action: skip copying this one (keep only the first)")

    print(f"\n--- Files to be copied into organized folders ---")
    for folder, files in plan["grouped"].items():
        print(f"  {dest}/{folder}/  <- {len(files)} file(s)")
        for f in files:
            print(f"      COPY '{f}'  ->  '{dest}/{folder}/{os.path.basename(f)}'")

    total_dupe_bytes = sum(os.path.getsize(d["duplicate"]) for d in plan["duplicates"])
    print(f"\nEstimated space reclaimable by not duplicating: {total_dupe_bytes} bytes")
    print("\nNo files have been moved, renamed, or deleted.")
    print("Re-run with --execute to approve and apply this exact plan.")
    print("=" * 60)


def execute_plan(plan, dest):
    os.makedirs(dest, exist_ok=True)
    for folder, files in plan["grouped"].items():
        target_folder = os.path.join(dest, folder)
        os.makedirs(target_folder, exist_ok=True)
        for f in files:
            target_path = os.path.join(target_folder, os.path.basename(f))
            shutil.copy2(f, target_path)  # copy, never move — originals untouched
            print(f"  ✅ copied '{f}' -> '{target_path}'")
    print(f"\nDone. Organized copy created at '{dest}/'. Originals in the source "
          f"folder were never modified, moved, or deleted.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python organize.py <folder> [--execute]")
        sys.exit(1)

    source = sys.argv[1]
    execute = "--execute" in sys.argv
    dest = os.path.join(os.path.dirname(source.rstrip("/")) or ".", "organized")

    plan = build_plan(source)

    if not execute:
        print_plan(plan, dest)
    else:
        print("Executing previously-reviewed plan...\n")
        execute_plan(plan, dest)


if __name__ == "__main__":
    main()
