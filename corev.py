import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("ml_dataset_no_pylint.csv") if 'ml_dataset_no_pylint.csv' in __import__('os').listdir('.') else pd.read_csv("ml_dataset.csv")
X = df[['radon_cc_total','pylint_msgs','bandit_issues_count']].fillna(0).astype(float)
y = df['is_fix_like'].astype(int)

pipe = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42))
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

y_pred = cross_val_predict(pipe, X, y, cv=cv, method='predict')
print(classification_report(y, y_pred, digits=4))
print("Confusion matrix (rows=true, cols=pred):")
print(confusion_matrix(y, y_pred))
