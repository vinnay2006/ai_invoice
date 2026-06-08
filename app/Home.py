import streamlit as st

st.set_page_config(
    page_title="AI Invoice Fraud Detection",
    layout="wide"
)

st.title("AI Invoice Fraud Detection System")

st.write(
    """
    Detect suspicious invoices using
    XGBoost, Isolation Forest and SHAP.
    """
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Invoices",
    "1050"
)

col2.metric(
    "Frauds",
    "50"
)

col3.metric(
    "Recall",
    "80%"
)

col4.metric(
    "ROC AUC",
    "0.94"
)