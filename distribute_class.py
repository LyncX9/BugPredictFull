import pandas as pd

DATASET_PATH = "ml_dataset.csv"
LABEL_COL = "is_fix_like"

df = pd.read_csv(DATASET_PATH)

class_counts = df[LABEL_COL].value_counts().sort_index()
class_ratio = df[LABEL_COL].value_counts(normalize=True).sort_index()

print("Class Counts:")
print(class_counts)

print("\nClass Ratio:")
print(class_ratio)

class_counts.to_csv("class_counts.csv")
class_ratio.to_csv("class_ratio.csv")
