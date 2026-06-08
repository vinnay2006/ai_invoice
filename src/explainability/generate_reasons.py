import joblib
import shap

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


def get_reasons_for_uploaded_data(X):

    explainer = shap.TreeExplainer(
        xgb_model
    )

    shap_values = explainer.shap_values(X)

    all_reasons = []

    for row_idx in range(len(X)):

        shap_row = shap_values[row_idx]

        positive_features = []

        for col_idx, value in enumerate(shap_row):

            if value > 0:

                positive_features.append(
                    (X.columns[col_idx], value)
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

        all_reasons.append(
            " | ".join(reasons)
        )

    return all_reasons