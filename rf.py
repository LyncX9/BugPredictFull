from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import pandas as pd
df = pd.read_csv("ml_dataset_no_pylint.csv") if 'ml_dataset_no_pylint.csv' in __import__('os').listdir('.') else pd.read_csv("ml_dataset.csv")
X = df[['radon_cc_total','pylint_msgs','bandit_issues_count']].fillna(0).astype(float)
y = df['is_fix_like'].astype(int)
pipe = make_pipeline(SimpleImputer(strategy='median'), StandardScaler())
Xs = pipe.fit_transform(X)
rf = RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42).fit(Xs, y)
importances = rf.feature_importances_
print(list(zip(['radon_cc_total','pylint_msgs','bandit_issues_count'], importances)))
