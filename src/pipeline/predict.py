import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from src.explainability.generate_reasons import (
    get_reasons_for_uploaded_data
)
xgb_model = joblib.load(
    "models/xgboost_model.pkl"
)

iso_model = joblib.load(
    "models/isolation_forest.pkl"
)


def predict_invoices(df):

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

    xgb_probs = xgb_model.predict_proba(X)[:, 1]

    iso_scores = iso_model.decision_function(X)

    scaler = MinMaxScaler()

    iso_scores_scaled = scaler.fit_transform(
        (-iso_scores).reshape(-1, 1)
    ).flatten()

    risk_score = (
        0.6 * xgb_probs +
        0.4 * iso_scores_scaled
    ) * 100

    df["risk_score"] = risk_score

    df["status"] = np.where(
        df["risk_score"] >= 70,
        "FLAGGED",
        "APPROVED"
    )
    df["reasons"] = get_reasons_for_uploaded_data(X)
    print("\nStatus Counts:")
    print(df["status"].value_counts())

    print("\nRisk Score Summary:")
    print(df["risk_score"].describe())

    print(df[["risk_score", "status", "reasons"]].head())
    return df
print("predict.py loaded successfully")