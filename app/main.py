import streamlit as st
from nlp import extract_signals
from risk_model import calculate_risk
from reasoning import generate_reasoning


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

    score, category = calculate_risk(signals)

    st.metric(label="Risk Score", value=score)
    st.metric(label="Risk Category", value=category)

    reasoning = generate_reasoning(signals, score, category)

    st.markdown("### Explanation")
    st.write(reasoning)

    st.markdown("### Recommended Action")
    if category == "High":
        st.write("Block transaction and escalate for manual review.")
    elif category == "Medium":
        st.write("Flag for additional verification.")
    else:
        st.write("Approve transaction.")
