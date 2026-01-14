import pandas as pd, subprocess, shlex, sys
df = pd.read_csv("ml_dataset.csv")
s0 = df.sample(6, random_state=42)
for i,row in s0.iterrows():
    sp = str(row['snapshot_path'])
    print("---- ROW:", i, "is_fix_like=", row['is_fix_like'], "file:", row['file_path_y'])
    try:
        with open(sp, "r", encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
            print("SNAPSHOT HEAD (first 40 lines):")
            for L in lines[:40]:
                print(L)
    except Exception as e:
        print("Cannot open snapshot:", e)
    cmds = [
        f"python -m radon cc -s -j \"{sp}\"",
        f"python -m pylint --output-format=json \"{sp}\"",
        f"python -m bandit -r \"{sp}\" -f json"
    ]
    for c in cmds:
        try:
            proc = subprocess.run(shlex.split(c), capture_output=True, text=True, timeout=30)
            out = proc.stdout.strip()
            err = proc.stderr.strip()
            print("CMD:", c)
            print("RC:", proc.returncode)
            if out:
                print("OUT:", out[:2000])
            if err:
                print("ERR:", err[:1000])
        except Exception as e:
            print("ERR RUN:", e)
    print("\n")
