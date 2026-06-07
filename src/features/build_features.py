import pandas as pd

df = pd.read_csv(
    "data/raw/invoices_with_fraud.csv"
)
#to find the duplicate records
df["is_duplicate"] = df.duplicated(
    subset=[
        "vendor_name",
        "invoice_number",
        "total_amount"
    ],
    keep=False
).astype(int)
print(df["is_duplicate"].value_counts())

#payment done close to the due date is again very suspicious 
df["invoice_date"] = pd.to_datetime(
    df["invoice_date"]
)

df["due_date"] = pd.to_datetime(
    df["due_date"]
)

df["days_to_due"] = (
    df["due_date"] - df["invoice_date"]
).dt.days
print(df["days_to_due"].describe())
#payment done on weekends which are usually off days
df["weekend_submission"] = (
    df["invoice_date"]
    .dt.dayofweek
    .isin([5, 6])
    .astype(int)
)
print(
    df["weekend_submission"]
    .value_counts()
)

#payments of amount just less then threshold to avoid extra scrutiny 
APPROVAL_LIMIT = 100000

df["amount_threshold_proximity"] = (
    APPROVAL_LIMIT
    - df["total_amount"]
).abs()

print(
    df["amount_threshold_proximity"]
    .sort_values()
    .head(20)
)

#checking the records for the consitency in the value unit_price*qty==total_amount
expected_total = (
    df["unit_price"]
    * df["quantity"]
)

df["line_item_price_consistency"] = (
    expected_total
    == df["total_amount"]
).astype(int)
print(
    df["line_item_price_consistency"]
    .value_counts()
)

df.to_csv(
    "data/processed/features_v1.csv",
    index=False
)