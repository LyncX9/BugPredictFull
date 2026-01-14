import json
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python function_risk.py <file.py>")
    sys.exit(1)

file_path = sys.argv[1]

cmd = [
    "python", "-m", "radon", "cc",
    "-s", "-j", file_path
]

proc = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(proc.stdout or "{}")

functions = []
for _, items in data.items():
    for it in items:
        if it["type"] == "method" or it["type"] == "function":
            functions.append({
                "name": it["name"],
                "complexity": it["complexity"],
                "rank": it["rank"],
                "line_start": it["lineno"],
                "line_end": it["endline"]
            })

functions.sort(key=lambda x: x["complexity"], reverse=True)

print("\n=== Risky Functions ===")
for f in functions[:5]:
    print(f"{f['name']} | CC={f['complexity']} | Rank={f['rank']} | Lines {f['line_start']}-{f['line_end']}")
print("\nDone.")