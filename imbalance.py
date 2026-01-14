import pandas as pd

df = pd.read_csv("ml_dataset.csv")

print("Total rows:", len(df))
print("\nLabel distribution:")
print(df['is_fix_like'].value_counts())
print("\nLabel distribution (percentage):")
print(df['is_fix_like'].value_counts(normalize=True))

print("\nFeature summary:")
print(df[['radon_cc_total','pylint_msgs','bandit_issues_count']].describe().T)
