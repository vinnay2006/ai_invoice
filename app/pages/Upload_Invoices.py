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
    st.session_state["results"] = result_df
    st.write(result_df.columns.tolist())
    flagged = result_df[
        result_df["status"] == "FLAGGED"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Invoices",
        len(result_df)
    )

    col2.metric(
        "Flagged",
        len(flagged)
    )

    col3.metric(
        "Flag Rate (%)",
        round(
            len(flagged) / len(result_df) * 100,
            2
        )
    ) 

    st.write("Results")

    st.dataframe(
        result_df[
            ["invoice_number", "risk_score", "status","reasons"]
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
            "status",
            "reasons"
        ]
    ]
)

    st.subheader("Flagged Invoice Reasons")

    for _, row in flagged.head(10).iterrows():

        st.write(
            f"Invoice: {row['invoice_number']}"
        )

        st.write(
            f"Risk Score: {row['risk_score']:.2f}"
        )

        st.write("Reasons:")

        for reason in row["reasons"].split("|"):
            st.write(f"• {reason.strip()}")

        st.divider()
    csv = result_df.to_csv(index=False)

    st.download_button(
        label="Download Results",
        data=csv,
        file_name="fraud_analysis_results.csv",
        mime="text/csv"
    )
