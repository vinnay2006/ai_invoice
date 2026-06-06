import pandas as pd
import random
df = pd.read_csv("data/raw/invoices_with_fraud.csv")
df = pd.read_csv("data/raw/invoices.csv")
fraud_count = int(len(df) * 0.05)
duplicate_rows = df.sample(
    n=10,
    random_state=42
).copy()

duplicate_rows["fraud"] = 1
df = pd.concat(
    [df, duplicate_rows],
    ignore_index=True
)
print(df["fraud"].value_counts())
df.to_csv(
    "data/raw/invoices_with_fraud.csv",
    index=False
)
#adding inflation in record and setting as fraud
clean_df = df[df["fraud"] == 0]
inflated_rows = clean_df.sample(
    n=10,
    random_state=1
).copy()
inflated_rows["total_amount"] = (
    inflated_rows["total_amount"] * 3
)
inflated_rows["tax_amount"] = (
    inflated_rows["total_amount"] * 0.18
)
inflated_rows["fraud"] = 1
df = pd.concat(
    [df, inflated_rows],
    ignore_index=True
)
df.to_csv(
    "data/raw/invoices_with_fraud.csv",
    index=False
)