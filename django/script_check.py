import pandas as pd
df = pd.read_csv("django_commits.csv")
print("Total rows:", len(df))
print("Unique commits:", df['commit_hash'].nunique())
print("Unique files:", df['file_path'].nunique())
print("Snapshots present:", df['snapshot_path'].notna().sum())
print("Fix-like rows:", df['is_fix_like'].sum(), "({:.2%})".format(df['is_fix_like'].mean()))
print(df[['commit_hash','commit_date','file_path','is_fix_like','snapshot_path']].sample(5).to_string(index=False))