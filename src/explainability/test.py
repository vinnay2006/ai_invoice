import pandas as pd

from src.explainability.generate_reasons import (
    get_reasons_for_uploaded_data
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

reasons = get_reasons_for_uploaded_data(X)
print(len(reasons))
print(len(X))
print(reasons[:5])