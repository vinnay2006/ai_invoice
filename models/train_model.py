import pandas as pd

df = pd.read_csv(
    "data/processed/features_v2.csv"
)


drop_cols = [
    "vendor_name",
    "vendor_id",
    "invoice_number",
    "invoice_date",
    "due_date",
    "bank_account",
    "department",
    "approver_name",
    "fraud"
]
X = df.drop(columns=drop_cols)

y = df["fraud"]
print(X.columns)
print(y.value_counts())

#doing the train/split data 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(X_train.shape)
print(X_test.shape)
print(y_train.value_counts())

from imblearn.over_sampling import SMOTE
smote = SMOTE(
    random_state=42
)

X_train_smote, y_train_smote = (
    smote.fit_resample(
        X_train,
        y_train
    )
)
print(y_train_smote.value_counts())
print(X_train_smote.shape)
print(y_train_smote.shape)
#training isolation forest -unsupervised learning 
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(
    contamination=0.05,
    random_state=42
)

iso_forest.fit(X_train)
iso_scores = iso_forest.decision_function(X_test)
print(iso_scores[:10])

#training the supersed model of learning XGBoost
from xgboost import XGBClassifier
xgb_model = XGBClassifier(
    random_state=42,
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    eval_metric="logloss"
)
xgb_model.fit(
    X_train_smote,
    y_train_smote
)
y_pred = xgb_model.predict(X_test)


y_prob = xgb_model.predict_proba(X_test)[:,1]

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1:", f1_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_prob))

print(classification_report(y_test, y_pred))

#tell which feature flagged the invoice
importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": xgb_model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print(importance)
import joblib

joblib.dump(
    iso_forest,
    "models/isolation_forest.pkl"
)

joblib.dump(
    xgb_model,
    "models/xgboost_model.pkl"
)

print("Models saved successfully")