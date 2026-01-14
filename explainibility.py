import joblib
import pandas as pd

pipe = joblib.load("best_model.joblib")

rf = pipe.named_steps["clf"]

features = [
    "radon_total_complexity",
    "radon_num_items",
    "pylint_msgs_count",
    "pylint_rc",
    "bandit_issues_count",
    "bandit_rc"
]

importances = pd.Series(
    rf.feature_importances_,
    index=features
).sort_values(ascending=False)

importances.to_csv("feature_importance.csv")

print("=== Feature Importance (RandomForest) ===")
print(importances)
print("Saved feature_importance.csv")