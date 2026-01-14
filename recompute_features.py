# recompute_features.py
import sys
from pathlib import Path
import csv
import json
import subprocess
import shlex
from multiprocessing import Pool, cpu_count
from functools import partial
import time

TIMEOUT = 60
WORKERS = max(1, cpu_count() - 1)
PROGRESS_INTERVAL = 100

def run_cmd(cmd, timeout=TIMEOUT):
    try:
        proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -2, "", str(e)

def process_file(root_snapshots: Path, file_path: Path):
    rel_path = file_path.relative_to(root_snapshots)
    snapshot_path_str = str(file_path)
    # Initialize defaults
    radon_total = 0
    radon_items = 0
    pylint_count = 0
    pylint_returncode = None
    bandit_count = 0
    bandit_returncode = None

    # radon: complexity JSON
    cmd_radon = f"python -m radon cc -s -j \"{snapshot_path_str}\""
    rc, out, err = run_cmd(cmd_radon)
    radon_return = rc
    if rc == 0 and out:
        try:
            parsed = json.loads(out)
            # parsed is dict {filename: [items...]}
            for k, items in parsed.items():
                for it in items:
                    if isinstance(it, dict) and "complexity" in it:
                        radon_total += int(it.get("complexity", 0))
                        radon_items += 1
        except Exception as e:
            # fallback: leave zeros
            pass

    # pylint: JSON list of messages -> count messages for this file
    cmd_pylint = f"python -m pylint --output-format=json \"{snapshot_path_str}\""
    rc, out, err = run_cmd(cmd_pylint)
    pylint_returncode = rc
    if out:
        try:
            parsed = json.loads(out)
            if isinstance(parsed, list):
                pylint_count = len(parsed)
        except Exception:
            # if JSON parse fails, fallback: try to count lines in stdout
            pylint_count = len(out.splitlines()) if out.strip() else 0

    # bandit: run per file, JSON results length
    cmd_bandit = f"python -m bandit -r \"{snapshot_path_str}\" -f json"
    rc, out, err = run_cmd(cmd_bandit)
    bandit_returncode = rc
    if out:
        try:
            parsed = json.loads(out)
            if isinstance(parsed, dict):
                results = parsed.get("results", [])
                # count results that point to this exact file
                bandit_count = sum(1 for r in results if Path(r.get("filename","")).name == file_path.name)
        except Exception:
            pass

    return {
        "snapshot_path": snapshot_path_str,
        "rel_path": str(rel_path),
        "radon_total_complexity": radon_total,
        "radon_num_items": radon_items,
        "pylint_msgs_count": pylint_count,
        "pylint_rc": pylint_returncode,
        "bandit_issues_count": bandit_count,
        "bandit_rc": bandit_returncode
    }

def discover_py_files(root_snapshots: Path):
    files = [p for p in root_snapshots.rglob("*.py") if p.is_file()]
    return files

def worker_init(args):
    pass

def main():
    if len(sys.argv) < 3:
        print("Usage: python recompute_features.py <snapshots_root> <out_csv>")
        sys.exit(1)
    root = Path(sys.argv[1])
    out_csv = Path(sys.argv[2])
    if not root.exists():
        print("Snapshots root not found:", root)
        sys.exit(1)

    files = discover_py_files(root)
    total = len(files)
    print(f"Discovered {total} python files under {root}. Workers: {WORKERS}")

    start = time.time()
    with Pool(WORKERS, initializer=worker_init, initargs=(None,)) as pool:
        func = partial(process_file, root)
        with out_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "snapshot_path","rel_path",
                "radon_total_complexity","radon_num_items",
                "pylint_msgs_count","pylint_rc",
                "bandit_issues_count","bandit_rc"
            ])
            processed = 0
            for res in pool.imap_unordered(func, files, chunksize=10):
                writer.writerow([
                    res["snapshot_path"], res["rel_path"],
                    res["radon_total_complexity"], res["radon_num_items"],
                    res["pylint_msgs_count"], res["pylint_rc"],
                    res["bandit_issues_count"], res["bandit_rc"]
                ])
                processed += 1
                if processed % PROGRESS_INTERVAL == 0 or processed == total:
                    elapsed = time.time() - start
                    rate = processed / elapsed if elapsed > 0 else 0
                    print(f"Processed {processed}/{total} files — {rate:.2f} files/s — elapsed {int(elapsed)}s")
    print("Done. Wrote", out_csv)

if __name__ == "__main__":
    main()
