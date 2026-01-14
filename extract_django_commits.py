import os
os.environ.setdefault("PYTHONUTF8", "1")
from pydriller import Repository
from datetime import datetime, timedelta
import csv
import sys
from pathlib import Path
import subprocess

if len(sys.argv) < 2:
    print("Usage: python extract_django_commits.py <repo_path> [out_csv]")
    sys.exit(1)

repo_path = sys.argv[1]
out_csv = sys.argv[2] if len(sys.argv) > 2 else "django_commits.csv"

since_years = 5
progress_interval = 50
max_files_threshold = 500
snapshot_enabled = True
only_snapshot_fix_like = False
snapshot_dir = Path("snapshots")

repo_dir = Path(repo_path)
if not repo_dir.exists():
    print("Repository path not found:", repo_dir)
    sys.exit(1)

since_date = datetime.now() - timedelta(days=since_years * 365)
keywords = ["fix", "bug", "patch", "resolve", "hotfix", "error", "issue"]

def extract_issue_ids(msg):
    ids = []
    for token in (msg or "").split():
        if token.startswith("#") and token[1:].isdigit():
            ids.append(token)
    return ";".join(ids)

def git_show(repo, commit, path):
    path = path.replace("\\", "/")
    cmd = ["git", "-C", str(repo), "show", f"{commit}:{path}"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if proc.returncode != 0:
            return None
        return proc.stdout
    except Exception:
        return None

rows_written = 0
commit_count = 0
failed_snapshots = 0

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["commit_hash", "commit_date", "author", "file_path", "is_fix_like", "snapshot_path"])
    print("Scanning repo:", repo_path)
    for commit in Repository(str(repo_dir), since=since_date).traverse_commits():
        commit_count += 1
        if commit_count % progress_interval == 0:
            print(f"Processed {commit_count} commits...")

        msg_raw = commit.msg or ""
        msg = msg_raw.lower()
        is_fix = any(k in msg for k in keywords) or extract_issue_ids(msg_raw) != ""

        modfiles = commit.modified_files
        if not modfiles:
            continue
        if len(modfiles) > max_files_threshold:
            continue

        for m in modfiles:
            if not m.filename or not m.filename.endswith(".py"):
                continue

            file_path = (m.new_path or m.old_path or m.filename).replace("\\", "/")
            snapshot_path = ""
            if snapshot_enabled and (not only_snapshot_fix_like or is_fix):
                content = git_show(repo_dir, commit.hash, file_path)
                if content:
                    target = snapshot_dir / commit.hash / file_path
                    try:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with open(target, "w", encoding="utf-8", errors="replace") as sf:
                            sf.write(content)
                        snapshot_path = str(target)
                    except Exception:
                        snapshot_path = ""
                        failed_snapshots += 1
                else:
                    failed_snapshots += 1

            author_name = commit.author.name if commit.author and commit.author.name else ""
            commit_date = commit.author_date.isoformat() if commit.author_date else ""

            w.writerow([commit.hash, commit_date, author_name, file_path, int(is_fix), snapshot_path])
            rows_written += 1

print(f"FINISHED. CSV: {out_csv}")
print(f"Commits processed: {commit_count}, rows written: {rows_written}, failed snapshots: {failed_snapshots}")
if snapshot_enabled:
    print("Snapshots saved under:", str(snapshot_dir.resolve()))
