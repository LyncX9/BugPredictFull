# move_snapshots_by_commits.py
import csv
from pathlib import Path
import shutil
import sys

if len(sys.argv) < 4:
    print("Usage: python move_snapshots_by_commits.py <commits_csv> <snapshots_root> <target_root>")
    print("Example: python move_snapshots_by_commits.py sklearn_commits.csv snapshots snapshots_sklearn")
    sys.exit(1)

commits_csv = Path(sys.argv[1])
snapshots_root = Path(sys.argv[2])
target_root = Path(sys.argv[3])

if not commits_csv.exists():
    print("Error: commits CSV not found:", commits_csv)
    sys.exit(1)
if not snapshots_root.exists():
    print("Error: snapshots root not found:", snapshots_root)
    sys.exit(1)

target_root.mkdir(parents=True, exist_ok=True)

# read unique commit hashes from CSV (fallback: try column names)
hashes = set()
with commits_csv.open("r", encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    if "commit_hash" not in reader.fieldnames:
        # fallback: try first column if header missing
        f.seek(0)
        for r in csv.reader(f):
            if r:
                hashes.add(r[0])
    else:
        for row in reader:
            h = row.get("commit_hash") or row.get("repo_commit") or ""
            if h:
                hashes.add(h.strip())

print(f"Found {len(hashes)} unique commit hashes in {commits_csv.name}")

moved = 0
missing = []
for h in hashes:
    src = snapshots_root / h
    dst = target_root / h
    if src.exists() and src.is_dir():
        # if dst exists, append suffix instead of overwriting
        if dst.exists():
            dst = Path(str(dst) + "_dup")
        try:
            shutil.move(str(src), str(dst))
            moved += 1
        except Exception as e:
            print("Failed to move", src, "->", dst, ":", e)
    else:
        missing.append(h)

print(f"Moved {moved} commit folders to {target_root}")
print(f"Missing (not found in snapshots root): {len(missing)}")
if missing:
    print("Sample missing (first 10):", missing[:10])
