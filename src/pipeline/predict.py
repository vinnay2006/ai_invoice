import joblib

xgb_model = joblib.load(
    "models/xgboost_model.pkl"
)

iso_model = joblib.load(
    "models/isolation_forest.pkl"
)

print("Models loaded")

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
xgb_probs = xgb_model.predict_proba(X)[:,1]

print(xgb_probs[:5])

iso_scores = iso_model.decision_function(X)

print(iso_scores[:5])

#convert the isolation values to risk score 
from sklearn.preprocessing import MinMaxScaler
import numpy as np

scaler = MinMaxScaler()

iso_scores_scaled = scaler.fit_transform(
    (-iso_scores).reshape(-1,1)
).flatten()
#used to create unified risk score 
risk_score = (
    0.6 * xgb_probs +
    0.4 * iso_scores_scaled
)

risk_score = risk_score * 100
df["risk_score"] = risk_score

df["status"] = np.where(
    df["risk_score"] >= 70,
    "FLAGGED",
    "APPROVED"
)

print(
    df[
        ["risk_score","status"]
    ].head(20)
)
print(
    df.groupby("status")["fraud"].value_counts()
)