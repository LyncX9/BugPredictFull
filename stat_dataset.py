import pandas as pd

df = pd.read_csv("ml_dataset.csv")

print("Total data:", len(df))
print(df['is_fix_like'].value_counts())
print(df['is_fix_like'].value_counts(normalize=True))
