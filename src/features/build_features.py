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