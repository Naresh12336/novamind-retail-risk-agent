import json
import random

from pathlib import Path
from datetime import datetime, timedelta

# ==========================================
# LOAD GLOBAL GEO DATA
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

GEO_FILE = (
    BASE_DIR / "data" / "global_geo_profiles.json"
)

with open(GEO_FILE, "r", encoding="utf-8") as f:
    GEO_REGIONS = json.load(f)

# ==========================================
# TEXT PATTERNS
# ==========================================
NORMAL_TEXT = [
    "normal purchase",
    "subscription renewal",
    "electronics order",
    "grocery payment",
    "monthly payment",
    "food delivery",
    "travel booking"
]

FRAUD_TEXT = [
    "refund urgently now",
    "urgent refund needed",
    "immediate payment reversal",
    "refund immediately",
    "payment failed urgent refund",
    "account locked refund needed",
    "chargeback immediately"
]

# ==========================================
# PERSONA TYPES
# ==========================================
PERSONA_TYPES = [
    "legit_user",
    "casual_risky",
    "refund_abuser",
    "fraud_ring",
    "account_takeover"
]


# ==========================================
# HELPERS
# ==========================================
def generate_timestamp():

    now = datetime.utcnow()

    return (
        now - timedelta(
            minutes=random.randint(0, 10000)
        )
    ).isoformat()


def choose_region_by_risk():

    regions = list(GEO_REGIONS.keys())

    weights = []

    for region in regions:
        weights.append(
            GEO_REGIONS[region]["fraud_rate"]
        )

    return random.choices(
        regions,
        weights=weights,
        k=1
    )[0]


def select_ip(region):

    if region not in GEO_REGIONS:
        region = random.choice(
            list(GEO_REGIONS.keys())
        )

    return random.choice(
        GEO_REGIONS[region]["ips"]
    )


# ==========================================
# PERSONA FACTORY
# ==========================================
def generate_persona(customer_id):

    persona = random.choice(
        PERSONA_TYPES
    )

    # --------------------------------------
    # LEGIT USER
    # --------------------------------------
    if persona == "legit_user":

        region = random.choice([
            "india",
            "usa",
            "canada",
            "uk",
            "japan",
            "australia"
        ])

        return {
            "persona": persona,

            "preferred_region": region,

            "device_stability": 0.95,

            "fraud_probability": 0.01,

            "refund_behavior": "low",

            "velocity_behavior": "normal",

            "shared_infrastructure": False,

            "preferred_text": NORMAL_TEXT
        }

    # --------------------------------------
    # CASUAL RISKY
    # --------------------------------------
    elif persona == "casual_risky":

        region = random.choice(
            list(GEO_REGIONS.keys())
        )

        return {
            "persona": persona,

            "preferred_region": region,

            "device_stability": 0.70,

            "fraud_probability": 0.20,

            "refund_behavior": "medium",

            "velocity_behavior": "moderate",

            "shared_infrastructure": False,

            "preferred_text": NORMAL_TEXT + FRAUD_TEXT
        }

    # --------------------------------------
    # REFUND ABUSER
    # --------------------------------------
    elif persona == "refund_abuser":

        region = choose_region_by_risk()

        return {
            "persona": persona,

            "preferred_region": region,

            "device_stability": 0.50,

            "fraud_probability": 0.75,

            "refund_behavior": "high",

            "velocity_behavior": "moderate",

            "shared_infrastructure": True,

            "preferred_text": FRAUD_TEXT
        }

    # --------------------------------------
    # FRAUD RING
    # --------------------------------------
    elif persona == "fraud_ring":

        region = choose_region_by_risk()

        return {
            "persona": persona,

            "preferred_region": region,

            "device_stability": 0.20,

            "fraud_probability": 0.95,

            "refund_behavior": "extreme",

            "velocity_behavior": "aggressive",

            "shared_infrastructure": True,

            "preferred_text": FRAUD_TEXT
        }

    # --------------------------------------
    # ACCOUNT TAKEOVER
    # --------------------------------------
    region = choose_region_by_risk()

    return {
        "persona": "account_takeover",

        "preferred_region": region,

        "device_stability": 0.10,

        "fraud_probability": 0.85,

        "refund_behavior": "medium",

        "velocity_behavior": "aggressive",

        "shared_infrastructure": False,

        "preferred_text": FRAUD_TEXT
    }