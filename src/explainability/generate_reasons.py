import pandas as pd
import joblib
import shap
import numpy as np

reason_map = {
    "bank_account_changed":
        "Vendor bank account differs from previous invoices",

    "is_duplicate":
        "Possible duplicate invoice detected",

    "price_deviation":
        "Invoice amount deviates from vendor history",

    "is_new_vendor":
        "Invoice submitted by a new vendor",

    "line_item_price_consistency":
        "Line item prices appear inconsistent",

    "weekend_submission":
        "Invoice submitted on weekend",

    "amount_threshold_proximity":
        "Amount is close to approval threshold"
}


xgb_model = joblib.load(
    "models/xgboost_model.pkl"
)

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

explainer = shap.TreeExplainer(
    xgb_model
)

shap_values = explainer.shap_values(X)

def get_top_reasons(invoice_idx):

    shap_row = shap_values[invoice_idx]

    positive_features = []

    for i, value in enumerate(shap_row):

        if value > 0:

            positive_features.append(
                (X.columns[i], value)
            )

    positive_features.sort(
        key=lambda x: x[1],
        reverse=True
    )

    reasons = []

    for feature, value in positive_features[:3]:

        if feature in reason_map:

            reasons.append(
                reason_map[feature]
            )

        else:

            reasons.append(feature)

    return reasons

invoice_idx = 1

reasons = get_top_reasons(invoice_idx)

print("\nFraud Reasons:\n")

for reason in reasons:
    print("-", reason)