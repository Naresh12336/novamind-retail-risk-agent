from pathlib import Path
import geoip2.database

from services.asn_reputation_service import (
    evaluate_dynamic_asn_risk
)

# ==========================================
# ASN DATABASE
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
ASN_DB_PATH = BASE_DIR / "data" / "GeoLite2-ASN.mmdb"

asn_reader = geoip2.database.Reader(str(ASN_DB_PATH))

# ==========================================
# BOOTSTRAP HEURISTICS
# ==========================================
HIGH_RISK_KEYWORDS = [
    "amazon",
    "aws",
    "google",
    "azure",
    "digitalocean",
    "ovh",
    "microsoft",
    "oracle",
    "vpn",
    "proxy",
    "hosting"
]


# ==========================================
# MAIN ASN ENGINE
# ==========================================
def evaluate_asn_risk(ip_address: str):

    if not ip_address:
        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    try:
        response = asn_reader.asn(ip_address)

        asn_number = response.autonomous_system_number
        organization = (
            response.autonomous_system_organization
            or "Unknown"
        )

        # ==================================
        # STATIC HEURISTIC SIGNALS
        # ==================================
        signals = []
        score = 0

        org_lower = organization.lower()

        for keyword in HIGH_RISK_KEYWORDS:

            if keyword in org_lower:
                signals.append("high_risk_hosting_asn")
                score += 10
                break

        # ==================================
        # DYNAMIC ASN REPUTATION
        # ==================================
        dynamic_result = evaluate_dynamic_asn_risk(
            asn_number
        )

        score += dynamic_result["score"]

        signals.extend(
            dynamic_result["signals"]
        )

        # deduplicate
        signals = list(set(signals))

        return {
            "score": score,
            "signals": signals,
            "profile": {
                "asn": asn_number,
                "organization": organization,
                "dynamic_profile": dynamic_result["profile"]
            }
        }

    except Exception as e:

        print("ASN ERROR:", str(e))

        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }