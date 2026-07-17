import random
from collections import defaultdict

from ml.persona_engine import (
    generate_persona,
    generate_timestamp,
    select_ip
)

# =====================================================
# SHARED FRAUD INFRASTRUCTURE
# =====================================================
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

# =====================================================
# CUSTOMER POOL
# =====================================================
CUSTOMER_POOL_SIZE = 1000

CUSTOMERS = [
    f"CUST_{i}"
    for i in range(1000,1000 + CUSTOMER_POOL_SIZE)
]

# =====================================================
# MERCHANT NETWORK
# =====================================================
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

# =====================================================
# TRANSACTION TYPES
# =====================================================
LEGIT_TRANSACTION_TYPES = [
    "purchase",
    "subscription",
    "bill_payment",
    "wallet_topup"
]

FRAUD_TRANSACTION_TYPES = [
    "purchase",
    "refund_request",
    "chargeback",
    "wallet_topup",
    "account_verification"
]

# =====================================================
# CUSTOMER STATE
# =====================================================
customer_memory = {}

customer_transaction_counter = defaultdict(int)

customer_campaign_state = defaultdict(bool)

customer_campaign_remaining = defaultdict(int)

# =====================================================
# HELPERS
# =====================================================
def chance(probability):

    return random.random() < probability


def weighted_choice(values, weights):

    return random.choices(
        values,
        weights=weights,
        k=1
    )[0]


def stable_or_rotate(base, stability):

    if chance(stability):
        return base

    return f"{base}_{random.randint(1,999)}"


def rotate_identifier(base,stability,suffix):

    if chance(stability):
        return base

    return (
        f"{base}_{suffix}_"
        f"{random.randint(1,999)}"
    )


def initialize_customer(persona):

    # -------------------------------------------------
    # Customer activity level
    # -------------------------------------------------
    persona["activity_level"] = weighted_choice(

        [
            "low",
            "medium",
            "high"
        ],

        [
            25,
            55,
            20
        ]

    )

    # -------------------------------------------------
    # Merchant loyalty
    # -------------------------------------------------
    persona["preferred_merchant"] = random.choice(MERCHANTS)

    # -------------------------------------------------
    # Stability scores
    # -------------------------------------------------
    persona["payment_stability"] = random.uniform(0.92,0.995)

    persona["browser_stability"] = random.uniform(0.88,0.99)

    persona["address_stability"] = random.uniform(0.97,0.999)

    # -------------------------------------------------
    # Fraud campaign probability
    # -------------------------------------------------
    persona["campaign_probability"] = random.uniform(0.05,0.20)

    return persona

# =====================================================
# CUSTOMER LIFECYCLE
# =====================================================
def update_campaign_state(customer_id, persona):

    # Existing campaign continues.
    if customer_campaign_state[customer_id]:

        customer_campaign_remaining[customer_id] -= 1

        if customer_campaign_remaining[customer_id] <= 0:

            customer_campaign_state[customer_id] = False

        return customer_campaign_state[customer_id]

    # Chance to begin a fraud campaign.
    if chance(persona["campaign_probability"]):

        customer_campaign_state[customer_id] = True

        customer_campaign_remaining[customer_id] = random.randint(
            2,
            6
        )

    return customer_campaign_state[customer_id]


# =====================================================
# FRAUD DECISION
# =====================================================
def decide_fraud(persona, campaign_active):

    probability = persona["fraud_probability"]

    if campaign_active:

        probability = min(
            0.95,
            probability * 3.5
        )

    return chance(probability)


# =====================================================
# MERCHANT SELECTION
# =====================================================
def choose_merchant(persona, fraud):

    preferred = persona["preferred_merchant"]

    if fraud and chance(0.30):

        return random.choice(HIGH_RISK_MERCHANTS)

    loyalty = random.random()

    if loyalty < 0.85:

        return preferred

    return random.choice(MERCHANTS)


# =====================================================
# TRANSACTION TYPE
# =====================================================
def choose_transaction_type(fraud):

    if fraud:

        return weighted_choice(

            FRAUD_TRANSACTION_TYPES,

            [
                40,
                20,
                15,
                15,
                10
            ]

        )

    return weighted_choice(

        LEGIT_TRANSACTION_TYPES,

        [
            65,
            15,
            10,
            10
        ]

    )


# =====================================================
# ACCOUNT AGE
# =====================================================
def choose_account_age(fraud):

    if fraud:

        if chance(0.70):

            return random.randint(1,90)

        return random.randint(91,2500)

    if chance(0.08):

        return random.randint(1,90)

    return random.randint(91,2500)


# =====================================================
# AMOUNT
# =====================================================
def choose_amount(fraud):

    if fraud:

        return weighted_choice(

            [

                random.randint(20,120),

                random.randint(120,500),

                random.randint(500,1500)

            ],

            [

                20,

                45,

                35

            ]

        )

    return weighted_choice(

        [

            random.randint(10,100),

            random.randint(100,400),

            random.randint(400,1200)

        ],

        [

            55,

            35,

            10

        ]

    )


# =====================================================
# REFUND HISTORY
# =====================================================
def choose_refunds(persona, fraud):

    behavior = persona["refund_behavior"]

    if behavior == "low":

        return random.randint(0,1)

    if behavior == "medium":

        if fraud:

            return random.randint(2,5)

        return random.randint(0,2)

    if behavior == "high":

        if fraud:

            return random.randint(4,8)

        return random.randint(1,3)

    if fraud:

        return random.randint(6,12)

    return random.randint(2,5)


# =====================================================
# DESCRIPTION
# =====================================================
def choose_description(persona, fraud):

    if fraud:

        return random.choice(persona["preferred_text"])

    normal = [

        text

        for text in persona["preferred_text"]

        if "refund" not in text.lower()

    ]

    if normal:

        return random.choice(normal)

    return random.choice(persona["preferred_text"])

# =====================================================
# CUSTOMER STATE MANAGEMENT
# =====================================================
def get_customer(customer_id):

    if customer_id not in customer_memory:

        persona = initialize_customer(generate_persona(customer_id))

        customer_memory[customer_id] = {

            "persona": persona,

            "state": {

                "device_id": f"DEV_{customer_id}",

                "payment_hash": f"PAY_{customer_id}",

                "browser_fp": f"BR_{customer_id}",

                "address_hash": f"ADDR_{customer_id}",

                "email_hash": f"MAIL_{customer_id}",

                "phone_hash": f"PH_{customer_id}",

                "transaction_count": 0,

                "last_merchant": persona["preferred_merchant"]

            }

        }

    return customer_memory[customer_id]


# =====================================================
# INFRASTRUCTURE EVOLUTION
# =====================================================
def evolve_customer_state(customer):

    persona = customer["persona"]

    state = customer["state"]

    state["transaction_count"] += 1

    # ------------------------------------------
    # Device replacement
    # ------------------------------------------
    state["device_id"] = rotate_identifier(

        state["device_id"],

        persona["device_stability"],

        "DEV"

    )

    # ------------------------------------------
    # Browser evolution
    # ------------------------------------------
    state["browser_fp"] = rotate_identifier(

        state["browser_fp"],

        persona["browser_stability"],

        "BR"

    )

    # ------------------------------------------
    # Payment evolution
    # ------------------------------------------
    state["payment_hash"] = rotate_identifier(

        state["payment_hash"],

        persona["payment_stability"],

        "PAY"

    )

    # ------------------------------------------
    # Address evolution
    # ------------------------------------------
    state["address_hash"] = rotate_identifier(

        state["address_hash"],

        persona["address_stability"],

        "ADDR"

    )

    return state


# =====================================================
# SHARED INFRASTRUCTURE
# =====================================================
def choose_infrastructure(persona,state,fraud):

    device = state["device_id"]

    payment = state["payment_hash"]

    address = state["address_hash"]

    browser = state["browser_fp"]

    # ------------------------------------------
    # Fraudsters only SOMETIMES reuse
    # infrastructure.
    # ------------------------------------------
    if fraud and persona["shared_infrastructure"]:

        if chance(0.55):

            device = random.choice(SHARED_DEVICES)

        if chance(0.45):

            payment = random.choice(SHARED_PAYMENTS)

        if chance(0.35):

            address = random.choice(SHARED_ADDRESSES)

        if chance(0.50):

            browser = random.choice(SHARED_BROWSERS)

    return {

        "device_id": device,

        "payment_hash": payment,

        "address_hash": address,

        "browser_fp": browser

    }


# =====================================================
# COMMUNICATION IDENTIFIERS
# =====================================================
def choose_contact_identifiers(state,fraud):

    email = state["email_hash"]

    phone = state["phone_hash"]

    if fraud:

        if chance(0.15):

            email = (
                f"MAIL_SHARED_"
                f"{random.randint(1,15)}"
            )

        if chance(0.10):

            phone = (
                f"PH_SHARED_"
                f"{random.randint(1,10)}"
            )

    return email, phone

# =====================================================
# MAIN TRANSACTION GENERATOR
# =====================================================
def generate_transaction(index):

    # -------------------------------------------------
    # CUSTOMER
    # -------------------------------------------------
    customer_id = random.choice(CUSTOMERS)

    customer = get_customer(customer_id)

    persona = customer["persona"]

    # -------------------------------------------------
    # UPDATE CUSTOMER HISTORY
    # -------------------------------------------------
    customer_transaction_counter[customer_id] += 1

    campaign_active = update_campaign_state(customer_id,persona)

    fraud = decide_fraud(persona,campaign_active)

    state = evolve_customer_state(customer)

    # -------------------------------------------------
    # MERCHANT
    # -------------------------------------------------
    merchant_id = choose_merchant(persona,fraud)

    state["last_merchant"] = merchant_id

    # -------------------------------------------------
    # GEO / IP
    # -------------------------------------------------
    region = persona["preferred_region"]

    ip_address = select_ip(region)

    # Fraud campaigns occasionally
    # reuse regional infrastructure.
    if campaign_active and chance(0.25):

        ip_address = select_ip(region)

    # -------------------------------------------------
    # INFRASTRUCTURE
    # -------------------------------------------------
    infra = choose_infrastructure(persona,state,fraud)

    # -------------------------------------------------
    # CONTACT INFORMATION
    # -------------------------------------------------
    email_hash, phone_hash = (choose_contact_identifiers(state,fraud))

    # -------------------------------------------------
    # TRANSACTION DETAILS
    # -------------------------------------------------
    tx_type = choose_transaction_type(fraud)

    description = choose_description(persona,fraud)

    amount = choose_amount(fraud)

    refunds = choose_refunds(persona,fraud)

    account_age = choose_account_age(fraud)

    # -------------------------------------------------
    # BUILD TRANSACTION
    # -------------------------------------------------
    transaction = {

        "transaction_id":f"SYN_{index}",

        "customer_id":customer_id,

        "merchant_id":merchant_id,

        "transaction_type":tx_type,

        "description":description,

        "amount": amount,

        "account_age_days":account_age,

        "refund_count_last_30_days":refunds,

        "timestamp":generate_timestamp(),

        "device_id":infra["device_id"],

        "ip_address":ip_address,

        "payment_method_hash":infra["payment_hash"],

        "shipping_address_hash":infra["address_hash"],

        "email_hash":email_hash,

        "phone_hash":phone_hash,

        "browser_fingerprint":infra["browser_fp"]

    }

    return transaction

# =====================================================
# BULK GENERATION
# =====================================================
def generate_dataset(size=1000):

    transactions = []

    for index in range(size):

        transaction = generate_transaction(index)

        transactions.append(transaction)

    return transactions