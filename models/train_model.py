import pandas as pd

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

y = df["fraud"]
print(X.columns)
print(y.value_counts())

#doing the train/split data 
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(X_train.shape)
print(X_test.shape)
print(y_train.value_counts())

from imblearn.over_sampling import SMOTE
smote = SMOTE(
    random_state=42
)

X_train_smote, y_train_smote = (
    smote.fit_resample(
        X_train,
        y_train
    )
)
print(y_train_smote.value_counts())
print(X_train_smote.shape)
print(y_train_smote.shape)