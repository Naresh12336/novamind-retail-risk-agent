import streamlit as st
from nlp import extract_signals

st.set_page_config(
    page_title="NovaMind – Retail Risk Agent",
    layout="centered"
)

st.title("NovaMind – Retail Risk Decision Agent")

st.markdown(
    """
    This system analyzes retail transactions and provides
    a risk assessment with an explanation.
    """
)

st.subheader("Transaction Input")

transaction_text = st.text_area(
    "Transaction Description",
    placeholder="Describe the transaction, customer behavior, or issue..."
)

transaction_type = st.selectbox(
    "Transaction Type",
    [
        "Purchase",
        "Refund Request",
        "Chargeback",
        "Vendor Inquiry",
        "Promotion Abuse"
    ]
)

if st.button("Analyze Risk"):
    signals = extract_signals(transaction_text)

    st.subheader("Extracted Signals")
    st.json(signals)

    st.metric(label="Risk Score", value="--")
    st.metric(label="Risk Category", value="--")

    st.markdown("### Explanation")
    st.write("NLP signals extracted. Risk scoring pending.")

    st.markdown("### Recommended Action")
    st.write("Pending analysis.")
