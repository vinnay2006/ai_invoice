import streamlit as st
import pandas as pd
import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

if project_root not in sys.path:
    sys.path.append(project_root)
from src.pipeline.predict import predict_invoices

st.title("Upload Invoices")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    result_df = predict_invoices(df)

    st.write("Results")

    st.dataframe(
        result_df[
            ["invoice_number", "risk_score", "status"]
        ]
    )

    st.write("Flagged Invoices")

    flagged = result_df[
        result_df["status"] == "FLAGGED"
    ]

    st.dataframe(
    flagged[
        [
            "invoice_number",
            "vendor_name",
            "total_amount",
            "risk_score",
            "status"
        ]
    ]
)