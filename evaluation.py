from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.read_csv("ml_dataset_no_pylint.csv") if 'ml_dataset_no_pylint.csv' in __import__('os').listdir('.') else pd.read_csv("ml_dataset.csv")
X = df[['radon_cc_total','pylint_msgs','bandit_issues_count']].fillna(0).astype(float)
y = df['is_fix_like'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
pipe = make_pipeline(SimpleImputer(strategy='median'), StandardScaler(), RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42))
pipe.fit(X_train, y_train)
yhat = pipe.predict(X_test)
print(classification_report(y_test, yhat))
