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

#risky vendor whse invoices occur more frequently in flagged cases
    st.subheader("Top Risky Vendors")

    vendor_counts = (
        flagged["vendor_name"]
        .value_counts()
        .head(10)
    )

    st.dataframe(vendor_counts)
    
    #now see the nice analyis using a chart
    import matplotlib.pyplot as plt
    st.subheader("Risk Score Distribution")

fig, ax = plt.subplots()

ax.hist(
    result_df["risk_score"],
    bins=20
)

st.pyplot(fig)

#graph for fraud vendor names st.subheader("Top Risky Vendors Chart")

st.subheader("Top Risky Vendors Chart")

fig, ax = plt.subplots()

vendor_counts.plot(
    kind="bar",
    ax=ax
)

st.pyplot(fig)