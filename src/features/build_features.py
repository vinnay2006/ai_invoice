import pandas as pd
from rapidfuzz import fuzz
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
#checking the mean deviation in the total_amount from his average usual
vendor_avg = (
    df.groupby("vendor_name")["total_amount"]
      .transform("mean")
)

df["price_deviation"] = (
    (df["total_amount"] - vendor_avg)
    / vendor_avg
)
print(
    df["price_deviation"]
    .describe()
)

#checking the new vendors for the first time
df = df.sort_values(
    "invoice_date"
)
df["is_new_vendor"] = (
    df.groupby("vendor_name")
      .cumcount()
      .eq(0)
      .astype(int)
)
print(
    df["is_new_vendor"]
    .value_counts()
)
#vendors who have changed the account name 
previous_bank = (
    df.groupby("vendor_name")
      ["bank_account"]
      .shift(1)
)
df["bank_account_changed"] = (
    df["bank_account"] != previous_bank
).astype(int)
df.loc[
    previous_bank.isna(),
    "bank_account_changed"
] = 0

print(
    df["bank_account_changed"]
    .value_counts()
)
#checking the invoice sequence _gap
df["invoice_numeric"] = (
    df["invoice_number"]
    .str.extract(r"(\d+)")
    .astype(int)
)
previous_invoice = (
    df.groupby("vendor_name")
      ["invoice_numeric"]
      .shift(1)
)
df["invoice_sequence_gap"] = (
    df["invoice_numeric"]
    - previous_invoice
)
df["invoice_sequence_gap"] = (
    df["invoice_sequence_gap"]
    .fillna(0)
)
print(
    df["invoice_sequence_gap"]
    .describe()
)
#knowing the vendor name suimilarity
approved_vendors = (
    df["vendor_name"]
    .unique()
    .tolist()
)
def max_similarity(name):
    return max(
        fuzz.ratio(name, vendor)
        for vendor in approved_vendors
    )

df["vendor_name_similarity"] = (
df["vendor_name"]
.apply(max_similarity)
)

print(
    df["vendor_name_similarity"]
    .describe()
)
df.to_csv(
    "data/processed/features_v2.csv",
    index=False
)