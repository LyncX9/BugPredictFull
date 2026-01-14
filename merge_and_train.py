import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
import json

commits_files = ["django_commits.csv", "sklearn_commits.csv"]   
features_files = ["features_corrected.csv", "features_sklearn.csv"]  
out_ml = "ml_dataset_all.csv"
preproc_file = "preproc.joblib"
best_model_file = "best_model.joblib"
cv_results_file = "cv_results_smote.json"
test_size = 0.2
random_state = 42
n_splits = 5
# For Windows stability: set n_jobs=1
cv_n_jobs = 1
train_n_jobs = 1

# ---- UTILS ----
def load_commits(paths):
    dfs = []
    for p in paths:
        if Path(p).exists():
            dfs.append(pd.read_csv(p, dtype=str))
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def load_features(paths):
    dfs = []
    for p in paths:
        if Path(p).exists():
            dfs.append(pd.read_csv(p, dtype=str))
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def normalize_paths(df, col):
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace("\\\\", "/", regex=False).str.replace("\\", "/", regex=False)
    return df

# ---- 1) load and merge on snapshot_path ----
commits = load_commits(commits_files)
features = load_features(features_files)

if commits.empty:
    raise SystemExit("No commits CSV found. Check commits_files list.")
if features.empty:
    raise SystemExit("No features CSV found. Check features_files list.")

commits = normalize_paths(commits, "snapshot_path")
features = normalize_paths(features, "snapshot_path")

# attempt to find common join column - use snapshot_path
merged = commits.merge(features, on="snapshot_path", how="inner", suffixes=("_commit","_feat"))
merged.to_csv(out_ml, index=False)
print("Merged rows:", len(merged))
print("Columns in merged:", merged.columns.tolist())

# ---- 2) basic cleanup and select numeric features ----
# adapt these column names to what your features CSV actually contains
numeric_cols_guess = [
    c for c in merged.columns
    if any(x in c.lower() for x in ["radon", "pylint", "bandit", "complexity", "count", "num", "score"])
]
# ensure label exists
if "is_fix_like" not in merged.columns:
    raise SystemExit("Label is_fix_like missing in merged dataset")

df = merged.copy()
df[numeric_cols_guess] = df[numeric_cols_guess].apply(pd.to_numeric, errors="coerce").fillna(0)

X = df[numeric_cols_guess]
y = df["is_fix_like"].astype(int)

# ---- 3) quick train/holdout split (stable eval) ----
X_train, X_hold, y_train, y_hold = train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_state)

# ---- 4) pipeline with SMOTE + scaler + classifier (use cv_n_jobs=1 on Windows) ----
models = {
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=random_state, n_jobs=train_n_jobs),
    "SVM": SVC(kernel="rbf", probability=True, random_state=random_state),
    "LogReg": LogisticRegression(max_iter=2000, random_state=random_state)
}

cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
results = {}

for name, clf in models.items():
    pipe = ImbPipeline([("smote", SMOTE(random_state=random_state)), ("scale", StandardScaler()), ("clf", clf)])
    sc = cross_validate(pipe, X_train, y_train, cv=cv, scoring=['accuracy','precision','recall','f1'], n_jobs=cv_n_jobs, return_train_score=False)
    results[name] = {k: float(sc[k].mean()) for k in sc if k.startswith("test_")}
    print(f"Model {name} CV ->", results[name])

# pick best model by test_f1 if present
best_name = max(results.keys(), key=lambda n: results[n].get("test_f1", 0.0))
best_clf = models[best_name]
best_pipe = ImbPipeline([("smote", SMOTE(random_state=random_state)), ("scale", StandardScaler()), ("clf", best_clf)])
best_pipe.fit(X_train, y_train)

# evaluate on holdout
from sklearn.metrics import classification_report, confusion_matrix
y_pred = best_pipe.predict(X_hold)
report = classification_report(y_hold, y_pred, output_dict=True)
cm = confusion_matrix(y_hold, y_pred).tolist()

# save artifacts
joblib.dump(best_pipe, best_model_file)
joblib.dump({"numeric_cols": numeric_cols_guess}, preproc_file)
with open(cv_results_file, "w") as fh:
    json.dump({"cv_results": results, "best_model": best_name, "holdout_report": report, "confusion_matrix": cm}, fh, indent=2)

print("Best model:", best_name)
print("Holdout report:", classification_report(y_hold, y_pred))
print("Saved:", best_model_file, preproc_file, cv_results_file)