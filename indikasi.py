import pandas as pd

df = pd.read_csv("ml_dataset.csv")

risk = df[
    (df["radon_total_complexity"] >= 10) |
    (df["pylint_msgs_count"] >= 5) |
    (df["bandit_issues_count"] >= 1)
].copy()

risk = risk.sort_values(
    ["radon_total_complexity", "bandit_issues_count", "pylint_msgs_count"],
    ascending=False
)

risk[[
    "file_path",
    "radon_total_complexity",
    "pylint_msgs_count",
    "bandit_issues_count"
]].head(20).to_csv("risky_files.csv", index=False)

print("Saved risky_files.csv")
