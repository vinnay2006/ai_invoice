import pandas as pd
import joblib
import shap

# Load model
xgb_model = joblib.load(
    "models/xgboost_model.pkl"
)

# Load data
df = pd.read_csv(
    "data/processed/features_v2.csv"
)

# Same columns used during training
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

# Create explainer
explainer = shap.TreeExplainer(
    xgb_model
)

# Generate SHAP values
shap_values = explainer.shap_values(X)

print("SHAP generated successfully")
shap.summary_plot(
    shap_values,
    X
)


invoice_idx = 1

print(
    X.iloc[invoice_idx]
)
shap.plots.waterfall(
    shap.Explanation(
        values=shap_values[invoice_idx],
        base_values=explainer.expected_value,
        data=X.iloc[invoice_idx],
        feature_names=X.columns
    )
)



