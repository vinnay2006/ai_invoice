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
#adding vendor_name spooling in record and setting as fraud
spoof_rows = clean_df.sample(
    n=10,
    random_state=3
).copy()

def spoof_vendor(name):
    name = name.replace("o", "0")
    name = name.replace("l", "1")
    name = name.replace("i", "1")
    return name

spoof_rows["vendor_name"] = (
    spoof_rows["vendor_name"]
    .apply(spoof_vendor)
)
spoof_rows["fraud"] = 1
df = pd.concat(
    [df, spoof_rows],
    ignore_index=True
)
df.to_csv(
    "data/raw/invoices_with_fraud.csv",
    index=False
)


#adding threshold proximity error  in record and setting as fraud
threshold_rows = clean_df.sample(
    n=10,
    random_state=4
).copy()

threshold_rows["total_amount"] = [
    random.choice(
        [99500, 99750, 99800, 99900, 99950]
    )
    for _ in range(len(threshold_rows))
]

threshold_rows["tax_amount"] = (
    threshold_rows["total_amount"] * 0.18
)
threshold_rows["fraud"] = 1
df = pd.concat(
    [df, threshold_rows],
    ignore_index=True
)
df.to_csv(
    "data/raw/invoices_with_fraud.csv",
    index=False
)

#adding fake account number fraud   in record and setting as fraud
bank_rows = clean_df.sample(
    n=10,
    random_state=5
).copy()

bank_rows["bank_account"] = (
    bank_rows["bank_account"]
    .astype(str)
    + "999"
)
bank_rows["fraud"] = 1
df = pd.concat(
    [df, bank_rows],
    ignore_index=True
)
df.to_csv(
    "data/raw/invoices_with_fraud.csv",
    index=False
)