from collections import defaultdict
from datetime import datetime
from pathlib import Path
import geoip2.database

# ==========================================
# DATABASE PATH
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "GeoLite2-City.mmdb"

reader = geoip2.database.Reader(str(DB_PATH))

# =========================================
# MEMORY STORE
# ==========================================
last_seen = defaultdict(dict)

HIGH_RISK_COUNTRIES = {
    "Unknown"
}

HIGH_RISK_ASN_KEYWORDS = [
    "hosting",
    "cloud",
    "vpn",
    "proxy",
    "digitalocean",
    "ovh",
    "aws",
    "azure"
]


# ==========================================
# HELPERS
# ==========================================
def geo_lookup(ip_address: str):

    try:
        response = reader.city(ip_address)

        return {
            "country": response.country.name or "Unknown",
            "city": response.city.name or "Unknown",
            "lat": response.location.latitude or 0,
            "lon": response.location.longitude or 0
        }

    except:
        return {
            "country": "Unknown",
            "city": "Unknown",
            "lat": 0,
            "lon": 0
        }


def hours_between(ts1: str, ts2: str):

    try:
        a = datetime.fromisoformat(ts1)
        b = datetime.fromisoformat(ts2)
        return abs((b - a).total_seconds()) / 3600
    except:
        return 999


def distance_km(lat1, lon1, lat2, lon2):
    return (((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5) * 111


# ==========================================
# MAIN ENGINE
# ==========================================
def evaluate_geo_risk(event: dict):

    customer_id = event.get("customer_id")
    ip = event.get("ip_address")
    timestamp = event.get("timestamp")

    if not customer_id or not ip:
        return {
            "score": 0,
            "signals": [],
            "profile": {}
        }

    current = geo_lookup(ip)

    signals = []
    score = 0

    # --------------------------------------
    # Unknown / risky country
    # --------------------------------------
    if current["country"] in HIGH_RISK_COUNTRIES:
        signals.append("unknown_country")
        score += 12

    previous = last_seen.get(customer_id)

    if previous:

        # new country anomaly
        if previous.get("country") != current["country"]:
            signals.append("new_country_access")
            score += 12

        hrs = hours_between(previous["timestamp"], timestamp)

        dist = distance_km(
            previous["lat"],
            previous["lon"],
            current["lat"],
            current["lon"]
        )

        # impossible travel
        if dist > 1500 and hrs < 2:
            signals.append("impossible_travel")
            score += 35

        # --------------------------------------
        # SAME COUNTRY MOVEMENT (NEW LOGIC)
        # --------------------------------------
        if previous and previous.get("country") == current["country"]:

            hrs = hours_between(previous["timestamp"], timestamp)

            dist = distance_km(
                previous["lat"],
                previous["lon"],
                current["lat"],
                current["lon"]
            )

            # fast long-distance movement within country
            if dist > 500 and hrs < 2:
                signals.append("rapid_geo_movement")
                score += 15

            # moderate anomaly
            elif dist > 300 and hrs < 1:
                signals.append("city_change_anomaly")
                score += 8

    # update memory
    last_seen[customer_id] = {
        "country": current["country"],
        "city": current["city"],
        "lat": current["lat"],
        "lon": current["lon"],
        "timestamp": timestamp
    }

    return {
        "score": score,
        "signals": signals,
        "profile": current
    }