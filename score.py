import pandas as pd
df = pd.read_csv("ml_dataset.csv")
if 'pylint_score' in df.columns and df['pylint_score'].isna().all():
    df = df.drop(columns=['pylint_score'])
    df.to_csv("ml_dataset_no_pylint.csv", index=False)
    print("Dropped pylint_score -> saved ml_dataset_no_pylint.csv")
else:
    print("pylint_score present or partially filled; not dropped")
