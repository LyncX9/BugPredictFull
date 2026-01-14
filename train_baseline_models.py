import pandas as pd
from joblib import load, dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression

pre = load("preproc.joblib")
info = pd.read_csv("dataset_info.csv")
ml = pd.read_csv("ml_dataset.csv")
cols = pre["X_cols"]
X = ml[cols].copy()
y = ml["is_fix_like"].astype(int).copy()
from sklearn.impute import SimpleImputer
imp = SimpleImputer(strategy="median")
X = imp.fit_transform(X)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X = sc.fit_transform(X)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
svm = SVC(kernel="rbf", C=1.0, gamma="scale", class_weight="balanced", probability=True)
lr = LogisticRegression(class_weight="balanced", max_iter=1000)
models = {"RandomForest": rf, "SVM": svm, "LogReg": lr}
results = {}
for name, m in models.items():
    scores = cross_validate(m, X, y, cv=cv, scoring=["accuracy","precision","recall","f1"], return_train_score=False)
    results[name] = {k: v.mean() for k, v in scores.items()}
dfres = pd.DataFrame(results).T
dfres.to_csv("cv_results.csv")
best_name = dfres["test_f1"].idxmax()
best_model = models[best_name]
best_model.fit(X, y)
dump(best_model, "best_model.joblib")
y_pred = best_model.predict(X)
cr = classification_report(y, y_pred, output_dict=True)
pd.DataFrame(cr).to_csv("classification_report_full.csv")
cm = confusion_matrix(y, y_pred)
pd.DataFrame(cm, index=["true_neg","true_pos"], columns=["pred_neg","pred_pos"]).to_csv("confusion_matrix.csv")
print("CV results:\n", dfres)
print("Best model:", best_name)
print("Saved best_model.joblib, cv_results.csv, classification_report_full.csv, confusion_matrix.csv")