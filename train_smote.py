import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

df = pd.read_csv("ml_dataset.csv")

X = df[['radon_total_complexity', 'radon_num_items', 'pylint_msgs_count', 'pylint_rc',
        'bandit_issues_count', 'bandit_rc']]
y = df['is_fix_like'].astype(int)

smote = SMOTE(random_state=42)

models = {
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42),
    "SVM": SVC(kernel="rbf", probability=True, random_state=42),
    "LogReg": LogisticRegression(max_iter=2000)
}

results = {}

for name, model in models.items():
    pipe = ImbPipeline([
        ('smote', SMOTE(random_state=42)),
        ('scale', StandardScaler()),
        ('clf', model)
    ])
    
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    
    scores = cross_validate(pipe, X, y, cv=cv,
                            scoring=['accuracy', 'precision', 'recall', 'f1'],
                            n_jobs=-1, return_train_score=False)
    
    results[name] = {
        'accuracy': scores['test_accuracy'].mean(),
        'precision': scores['test_precision'].mean(),
        'recall': scores['test_recall'].mean(),
        'f1': scores['test_f1'].mean(),
    }

print("\n=== SMOTE Training Results ===")
for name, metrics in results.items():
    print(f"\nModel: {name}")
    for m, v in metrics.items():
        print(f"  {m}: {v:.4f}")
