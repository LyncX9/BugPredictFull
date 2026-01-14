import pandas as pd

df = pd.read_csv("ml_dataset.csv")

features = [
    "radon_total_complexity",
    "radon_num_items",
    "pylint_msgs_count",
    "pylint_rc",
    "bandit_issues_count",
    "bandit_rc"
]

stats = df[features].describe()
print(stats)

stats.to_csv("statistik_fitur.csv")
