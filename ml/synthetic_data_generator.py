import random

from ml.persona_engine import (
    generate_persona,
    generate_timestamp,
    select_ip
)

# ==========================================
# SHARED FRAUD INFRASTRUCTURE
# ==========================================
SHARED_DEVICES = [
    "SHARED_DEV_1",
    "SHARED_DEV_2",
    "SHARED_DEV_3"
]

SHARED_PAYMENTS = [
    "SHARED_PAY_1",
    "SHARED_PAY_2"
]

SHARED_ADDRESSES = [
    "SHARED_ADDR_1",
    "SHARED_ADDR_2"
]

SHARED_BROWSERS = [
    "SHARED_BR_1",
    "SHARED_BR_2"
]

# ==========================================
# CUSTOMER POOL
# ==========================================
CUSTOMER_POOL_SIZE = 1000

CUSTOMERS = [

    f"CUST_{i}"

    for i in range(
        1000,
        1000 + CUSTOMER_POOL_SIZE
    )

]

# ==========================================
# MERCHANT NETWORK
# ==========================================
MERCHANTS = [
    "MERCHANT_AMAZON",
    "MERCHANT_FLIPKART",
    "MERCHANT_MYNTRA",
    "MERCHANT_CROMA",
    "MERCHANT_RELIANCE",
    "MERCHANT_NYKAA",
    "MERCHANT_BIGBASKET",
    "MERCHANT_ZEPTO",
    "MERCHANT_SWIGGY",
    "MERCHANT_ZOMATO"
]

HIGH_RISK_MERCHANTS = [
    "MERCHANT_UNKNOWN_1",
    "MERCHANT_UNKNOWN_2",
    "MERCHANT_UNKNOWN_3"
]

# ==========================================
# CUSTOMER MEMORY
# ==========================================
customer_memory = {}


# ==========================================
# HELPERS
# ==========================================
def stable_or_rotate(base, stability):

    if random.random() < stability:
        return base

    return f"{base}_{random.randint(1,999)}"


# ==========================================
# MAIN GENERATOR
# ==========================================
def generate_transaction(index):
    customer_id = random.choice(CUSTOMERS)

    # --------------------------------------
    # PERSIST PERSONA
    # --------------------------------------
    if customer_id not in customer_memory:
        persona = generate_persona(customer_id)

        persona["preferred_merchant"] = random.choice(MERCHANTS)

        customer_memory[customer_id] = persona

    persona = customer_memory[customer_id]

    # --------------------------------------
    # FRAUD DECISION
    # --------------------------------------
    fraud = (random.random()< persona["fraud_probability"])

    # --------------------------------------
    # MERCHANT
    # --------------------------------------
    merchant_id = persona["preferred_merchant"]

    # Fraudsters occasionally migrate
    # to risky merchants.
    if fraud and random.random() < 0.35:

        merchant_id = random.choice(HIGH_RISK_MERCHANTS)

    # Legitimate customers occasionally
    # shop elsewhere.
    elif random.random() < 0.15:

        merchant_id = random.choice(MERCHANTS)

    # --------------------------------------
    # GEO / IP
    # --------------------------------------
    region = persona["preferred_region"]

    ip_address = select_ip(region)

    # --------------------------------------
    # DEVICE STABILITY
    # --------------------------------------
    base_device = (f"DEV_{customer_id}"
    )

    device_id = stable_or_rotate(
        base_device,
        persona["device_stability"]
    )

    # --------------------------------------
    # SHARED INFRA
    # --------------------------------------
    if persona["shared_infrastructure"]:

        device_id = random.choice(
            SHARED_DEVICES
        )

        payment_hash = random.choice(
            SHARED_PAYMENTS
        )

        address_hash = random.choice(
            SHARED_ADDRESSES
        )

        browser_fp = random.choice(
            SHARED_BROWSERS
        )

    else:

        payment_hash = (
            f"PAY_{customer_id}"
        )

        address_hash = (
            f"ADDR_{customer_id}"
        )

        browser_fp = (
            f"BR_{customer_id}"
        )

    # --------------------------------------
    # TEXT
    # --------------------------------------
    description = random.choice(
        persona["preferred_text"]
    )

    # --------------------------------------
    # ACCOUNT AGE
    # --------------------------------------
    if fraud:
        account_age_days = random.randint(1, 30)
    else:
        account_age_days = random.randint(
            100,
            2000
        )

    # --------------------------------------
    # REFUNDS
    # --------------------------------------
    refund_behavior = (
        persona["refund_behavior"]
    )

    if refund_behavior == "low":
        refunds = random.randint(0, 1)

    elif refund_behavior == "medium":
        refunds = random.randint(1, 3)

    elif refund_behavior == "high":
        refunds = random.randint(3, 6)

    else:
        refunds = random.randint(6, 12)

    # --------------------------------------
    # AMOUNT
    # --------------------------------------
    if fraud:
        amount = random.randint(120, 800)
    else:
        amount = random.randint(10, 120)

    # --------------------------------------
    # TRANSACTION TYPE
    # --------------------------------------
    tx_type = (
        "refund_request"
        if fraud
        else "purchase"
    )

    return {
        "transaction_id": f"SYN_{index}",

        "customer_id": customer_id,

        "merchant_id": merchant_id,

        "transaction_type": tx_type,

        "description": description,

        "amount": amount,

        "account_age_days": account_age_days,

        "refund_count_last_30_days": refunds,

        "timestamp": generate_timestamp(),

        "device_id": device_id,

        "ip_address": ip_address,

        "payment_method_hash": payment_hash,

        "shipping_address_hash": address_hash,

        "email_hash": (
            f"MAIL_{customer_id}"
        ),

        "phone_hash": (
            f"PH_{customer_id}"
        ),

        "browser_fingerprint": browser_fp
    }


# ==========================================
# BULK GENERATION
# ==========================================
def generate_dataset(size=1000):

    transactions = []

    for i in range(size):

        tx = generate_transaction(i)

        transactions.append(tx)

    return transactions