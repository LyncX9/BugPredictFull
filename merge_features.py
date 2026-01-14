import pandas as pd
from pathlib import Path
a = pd.read_csv("django_commits.csv")
b = pd.read_csv("features_corrected.csv")
a['snapshot_path'] = a['snapshot_path'].astype(str)
b['snapshot_path'] = b['snapshot_path'].astype(str)
merged = a.merge(b, left_on="snapshot_path", right_on="snapshot_path", how="inner")
merged.to_csv("ml_dataset.csv", index=False)
print("Merged rows:", len(merged))
print("Buggy fraction:", merged['is_fix_like'].mean())
print("Done -> ml_dataset.csv")