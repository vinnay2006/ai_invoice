import pandas as pd
import random
from faker import Faker
fake=Faker()
invoices=[]
for i in range(100):
    vendor_name = fake.company()
    vendor_id = random.randint(1000, 9999)
    invoice_number = f"INV-{random.randint(10000,99999)}"

    unit_price = random.randint(100,5000)
    quantity = random.randint(1,20)

    total_amount = unit_price * quantity
    tax_amount = total_amount * 0.18

    invoice = {
        "vendor_name": vendor_name,
        "vendor_id": vendor_id,
        "invoice_number": invoice_number,
        "unit_price": unit_price,
        "quantity": quantity,
        "total_amount": total_amount,
        "tax_amount": tax_amount,
        "fraud": 0
    }
    invoices.append(invoice)
    df=pd.DataFrame(invoices)
    print(df.head())
    df.to_csv(
        "data/raw/invoices.csv",
        index=False
    )
