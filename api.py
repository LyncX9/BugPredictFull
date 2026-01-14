from fastapi import FastAPI
import joblib
import pandas as pd
import subprocess
import json
import tempfile

app = FastAPI()

model = joblib.load("best_model.joblib")
preproc = joblib.load("preproc.joblib")

@app.post("/predict")
def predict(code: str):
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
        f.write(code.encode("utf-8"))
        tmp_path = f.name

    features = subprocess.run(
        ["python", "run_sca_parallel.py", tmp_path],
        capture_output=True,
        text=True
    )

    df = pd.read_csv("tmp_features.csv")
    X = df[preproc.feature_names_in_]

    prob = model.predict_proba(X)[0][1]

    return {
        "label": "BUG-FIX LIKELY" if prob > 0.5 else "NON-BUG",
        "probability": float(prob)
    }
