import sys
import joblib
import pandas as pd
from pathlib import Path
import subprocess
import json

MODEL_PATH = "best_model.joblib"
FEATURES = [
    "radon_total_complexity",
    "radon_num_items",
    "pylint_msgs_count",
    "pylint_rc",
    "bandit_issues_count",
    "bandit_rc",
]

def safe_float(x):
    if x is None:
        return 0.0
    if isinstance(x, (list, tuple)):
        return float(x[0]) if len(x) > 0 else 0.0
    if hasattr(x, "item"):
        return float(x.item())
    return float(x)

def run_cmd(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if p.returncode != 0:
            return None
        return p.stdout
    except Exception:
        return None

def extract_features(file_path):
    features = dict.fromkeys(FEATURES, 0.0)

    radon_out = run_cmd(["python", "-m", "radon", "cc", "-s", "-j", file_path])
    if radon_out:
        data = json.loads(radon_out)
        items = list(data.values())[0] if data else []
        features["radon_num_items"] = len(items)
        features["radon_total_complexity"] = sum(i.get("complexity", 0) for i in items)

    pylint_out = run_cmd(["python", "-m", "pylint", "--output-format=json", file_path])
    if pylint_out:
        msgs = json.loads(pylint_out)
        features["pylint_msgs_count"] = len(msgs)
        features["pylint_rc"] = 1 if len(msgs) == 0 else 0

    bandit_out = run_cmd(["python", "-m", "bandit", "-r", file_path, "-f", "json"])
    if bandit_out:
        data = json.loads(bandit_out)
        issues = data.get("results", [])
        features["bandit_issues_count"] = len(issues)
        features["bandit_rc"] = 1 if len(issues) == 0 else 0

    return features

def extract_hotspots(file_path, threshold=10):
    radon_out = run_cmd(["python", "-m", "radon", "cc", "-s", "-j", file_path])
    risky = []
    if radon_out:
        data = json.loads(radon_out)
        items = list(data.values())[0] if data else []
        for i in items:
            if i.get("complexity", 0) >= threshold:
                risky.append({
                    "function": i.get("name"),
                    "line": i.get("lineno"),
                    "complexity": i.get("complexity"),
                })
    return risky

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict_with_hotspot.py <file.py>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print("File not found:", file_path)
        sys.exit(1)

    model = joblib.load(MODEL_PATH)

    raw_features = extract_features(file_path)

    X = pd.DataFrame([{
        f: safe_float(raw_features.get(f, 0))
        for f in FEATURES
    }])

    proba = model.predict_proba(X)[0][1]
    label = "BUG-FIX LIKELY" if proba >= 0.5 else "NON-BUG"

    hotspots = extract_hotspots(file_path)

    print("\n=== Bug Prediction Result ===")
    print("File:", file_path)
    print("Label:", label)
    print("Probability:", round(proba, 4))

    if hotspots:
        print("\n⚠️  Risky Functions:")
        for h in hotspots:
            print(f"- {h['function']} (line {h['line']}, CC={h['complexity']})")
    else:
        print("\nNo high-risk functions detected.")

    print("\nDone.")
