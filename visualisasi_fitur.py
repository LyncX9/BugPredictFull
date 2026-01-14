import pandas as pd
import matplotlib.pyplot as plt

features = [
    "radon_total_complexity",
    "radon_num_items",
    "pylint_msgs_count",
    "bandit_issues_count"
]

df = pd.read_csv("ml_dataset.csv")

for f in features:
    plt.figure()
    df[f].hist(bins=30)
    plt.title(f"Distribusi {f}")
    plt.xlabel(f)
    plt.ylabel("Frekuensi")
    plt.tight_layout()
    plt.savefig(f"hist_{f}.png")
    plt.show()
