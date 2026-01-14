import pandas as pd, os
df = pd.read_csv("ml_dataset.csv")
df['snapshot_path'] = df['snapshot_path'].astype(str)
df = df[~df['file_path_y'].str.lower().str.contains(r'(^|/)tests?(/|$)|/test_|/examples/|/docs/')]

def strict_fix(msg, is_fix):
    ks = ["fix","bug","patch","hotfix","resolve"]
    msgl = (msg or "").lower()
    has_kw = any(k in msgl for k in ks)
    has_issue = "#" in (msg or "")
    return int(is_fix and (has_kw or has_issue))

df['is_fix_strict'] = df.apply(lambda r: strict_fix(r['commit_msg'] if 'commit_msg' in r.index else r.get('commit_msg',''), r['is_fix_like']), axis=1)
df = df[df['snapshot_path']!="" ]
counts = df['is_fix_strict'].value_counts()
minclass = counts.min()
df_balanced = pd.concat([df[df['is_fix_strict']==1].sample(minclass, random_state=42),
                         df[df['is_fix_strict']==0].sample(minclass, random_state=42)], ignore_index=True)
df.to_csv("ml_dataset_filtered.csv", index=False)
df_balanced.to_csv("ml_dataset_balanced.csv", index=False)
print("Filtered rows:", len(df), "Balanced rows:", len(df_balanced))
print("Counts filtered:", df['is_fix_strict'].value_counts().to_dict())
