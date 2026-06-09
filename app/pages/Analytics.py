#risky vendor whse invoices occur more frequently in flagged cases
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
if "results" not in st.session_state:

    st.warning(
        "Please upload invoices first."
    )

    st.stop()

result_df = st.session_state["results"]

flagged = result_df[
    result_df["status"] == "FLAGGED"
]

#now we want to group the methods of frauds 
from collections import Counter

reason_counter = Counter()

for reasons in flagged["reasons"]:

    reason_list = reasons.split("|")

    for reason in reason_list:

        reason_counter[
            reason.strip()
        ] += 1

reason_df = pd.DataFrame(
    reason_counter.items(),
    columns=[
        "Reason",
        "Count"
    ]
)

reason_df = reason_df.sort_values(
    by="Count",
    ascending=False
)

st.subheader(
    "Top Fraud Indicators"
)

st.dataframe(reason_df)

fig, ax = plt.subplots()

reason_df.head(10).plot(
    x="Reason",
    y="Count",
    kind="bar",
    ax=ax
)

st.pyplot(fig)

#plot for the risk distribution 
st.subheader(
    "Risk Band Distribution"
)

st.bar_chart(
    result_df[
        "risk_band"
    ].value_counts()
)
#------------------------------------
st.subheader("Top Risky Vendors")

vendor_counts = (
    flagged["vendor_name"]
    .value_counts()
    .head(10)
)

st.dataframe(vendor_counts)

#now see the nice analyis using a chart

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