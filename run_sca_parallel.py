from pathlib import Path
from multiprocessing import Pool, cpu_count
import subprocess, shlex, json, csv, sys

snapshots_root = Path("snapshots")
out_csv = Path("features_parallel.csv")
files = list(snapshots_root.rglob("*.py"))
def run_cmd(cmd):
    proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr
def process_file(path):
    p = Path(path)
    rel = p.relative_to(snapshots_root)
    repo_commit = p.parts[0] if len(p.parts)>0 else ""
    file_path = str(rel)
    pylint_score = ""
    pylint_msgs = 0
    radon_cc = ""
    bandit_count = 0
    try:
        rc,out,err = run_cmd(f"python -m pylint --output-format=json {str(p)}")
        if out.strip():
            j = json.loads(out)
            pylint_msgs = len(j)
        rc2,out2,err2 = run_cmd(f"python -m pylint --score=y {str(p)}")
        if out2:
            for line in out2.splitlines():
                if "Your code has been rated at" in line:
                    parts = line.split()
                    if len(parts)>=6:
                        pylint_score = parts[5]
                        break
    except:
        pass
    try:
        rc,out,err = run_cmd(f"python -m radon cc -s -j {str(p)}")
        if out.strip():
            j = json.loads(out)
            total_cc = 0
            for funcs in j.values():
                for item in funcs:
                    total_cc += int(item.get("complexity",0))
            radon_cc = total_cc
    except:
        radon_cc = ""
    try:
        rc,out,err = run_cmd(f"python -m bandit -r {str(p)} -f json")
        if out.strip():
            j = json.loads(out)
            bandit_count = len(j.get("results",[]))
    except:
        bandit_count = 0
    return [str(p), repo_commit, file_path, pylint_score, pylint_msgs, radon_cc, bandit_count]

if __name__ == "__main__":
    if not snapshots_root.exists():
        print("snapshots folder not found. ensure extract step produced snapshots.")
        sys.exit(1)
    nproc = max(1, cpu_count()-1)
    pool = Pool(nproc)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["snapshot_path","repo_commit","file_path","pylint_score","pylint_msgs","radon_cc_total","bandit_issues_count"])
        for row in pool.imap_unordered(process_file, files):
            writer.writerow(row)
    pool.close()
    pool.join()
    print("Features written to", out_csv)