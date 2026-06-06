import pandas as pd
import random
from faker import Faker
from datetime import timedelta
fake=Faker()
invoices=[]
vendors = []

for i in range(50):
    vendors.append({
        "vendor_name": fake.company(),
        "vendor_id": f"V{i+1:03}",
        "bank_account": fake.bban()
     })
for i in range(1000):
    vendor = random.choice(vendors)

    vendor_name = vendor["vendor_name"]
    vendor_id = vendor["vendor_id"]
    bank_account = vendor["bank_account"]
    invoice_number = f"INV-{random.randint(10000,99999)}"

    unit_price = random.randint(100,5000)
    quantity = random.randint(1,20)

    total_amount = unit_price * quantity
    tax_amount = total_amount * 0.18
    invoice_date = fake.date_between(start_date="-1y", end_date="today")

    payment_terms = random.choice([15, 30, 45, 60])

    due_date = invoice_date + timedelta(days=payment_terms)

    bank_account = fake.bban()

    department = random.choice([
        "Finance",
        "IT",
        "HR",
        "Procurement",
        "Operations"
    ])
    
    approver_name = fake.name()

    invoice = {
        "vendor_name": vendor_name,
        "vendor_id": vendor_id,
        "bank_account":bank_account,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "unit_price": unit_price,
        "quantity": quantity,
        "total_amount": total_amount,
        "tax_amount": tax_amount,
        "payment_terms": payment_terms,
        "bank_account": bank_account,
        "department": department,
        "approver_name": approver_name,
        "fraud": 0
    }
    invoices.append(invoice)
    df=pd.DataFrame(invoices)
   

    df.to_csv(
        "data/raw/invoices.csv",
        index=False
    )
print(df.isnull().sum())
print(df["vendor_name"].value_counts().head())
