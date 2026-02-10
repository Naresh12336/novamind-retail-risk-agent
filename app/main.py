import streamlit as st

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
    if not transaction_text.strip():
        st.warning("Please enter a transaction description.")
    else:
        st.subheader("Risk Assessment Result")

        st.metric(label="Risk Score", value="--")
        st.metric(label="Risk Category", value="--")

        st.markdown("### Explanation")
        st.write("Risk analysis will appear here.")

        st.markdown("### Recommended Action")
        st.write("Pending analysis.")
