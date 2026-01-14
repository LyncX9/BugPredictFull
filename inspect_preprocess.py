import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from joblib import dump

p = Path("ml_dataset.csv")
df = pd.read_csv(p)

df.columns = [c.strip() for c in df.columns]
rename_map = {}
for c in df.columns:
    if c.lower().startswith("pylint_score"):
        rename_map[c] = "pylint_score"
if "pylint_scoree" in df.columns:
    rename_map["pylint_scoree"] = "pylint_score"
if rename_map:
    df = df.rename(columns=rename_map)

expected = ["is_fix_like","radon_cc_total","pylint_msgs","bandit_issues_count"]
present = [c for c in expected if c in df.columns]
print("Total rows:", len(df))
print("Columns:", df.columns.tolist())
print("Present expected numeric features:", present)
print("Missing per column:\n", df.isna().sum())

df = df.dropna(subset=["is_fix_like"])
df["is_fix_like"] = df["is_fix_like"].astype(int)

numeric_feats = [c for c in ["radon_cc_total","pylint_msgs","bandit_issues_count","pylint_score"] if c in df.columns]
X = df[numeric_feats].copy()
y = df["is_fix_like"].copy()

imp = SimpleImputer(strategy="median")
scaler = StandardScaler()
pipeline = make_pipeline(imp, scaler)
Xs = pipeline.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(Xs, y, stratify=y, test_size=0.2, random_state=42)

dump({"pipeline": pipeline, "X_cols": numeric_feats}, "preproc.joblib")
pd.DataFrame({"n_rows":[len(df)], "n_features":[len(numeric_feats)], "buggy_fraction":[y.mean()]}).to_csv("dataset_info.csv", index=False)
print("Saved preproc.joblib and dataset_info.csv")
