#risky vendor whse invoices occur more frequently in flagged cases
import streamlit as st
import pandas as pd

if "results" not in st.session_state:

    st.warning(
        "Please upload invoices first."
    )

    st.stop()

result_df = st.session_state["results"]
st.write(result_df.columns.tolist())

flagged = result_df[
    result_df["status"] == "FLAGGED"
]
#invoice drill down 
st.subheader(
    " Choose Invoice For Investigation"
)

selected_invoice = st.selectbox(
    "Select Invoice",
    result_df["invoice_number"]
)

invoice = result_df[
    result_df["invoice_number"]
    == selected_invoice
].iloc[0]

st.write(
    f"Vendor: {invoice['vendor_name']}"
)

st.write(
    f"Amount: {invoice['total_amount']}"
)

st.write(
    f"Risk Score: {invoice['risk_score']:.2f}"
)

st.write(
    f"Risk Band: {invoice['risk_band']}"
)

st.write(
    f"Status: {invoice['status']}"
)

st.write("Reasons:")
for reason in invoice["reasons"].split("|"):

    st.write(
        f"• {reason.strip()}"
    )
