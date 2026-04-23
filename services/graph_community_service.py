from collections import defaultdict, deque
from pathlib import Path
import json
# graph_community_service.py

# DEPRECATED FILE
# kept only for backward compatibility

from services.graph_service import detect_fraud_community
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "decision_history.jsonl"
# ==============================
# ENTITY INDEXES (shared graph)
# ==============================
device_index = defaultdict(set)
ip_index = defaultdict(set)
payment_index = defaultdict(set)
address_index = defaultdict(set)
email_index = defaultdict(set)
phone_index = defaultdict(set)
browser_index = defaultdict(set)

# reverse mapping (customer → entities)
customer_entities = defaultdict(dict)

# ==============================
# THRESHOLDS
# ==============================
COMMUNITY_MIN_SIZE = 4


# ==============================
# GRAPH UPDATE
# ==============================
def update_graph(event: dict):

    customer = event.get("customer_id")

    entity_map = {
        "device": event.get("device_id"),
        "ip": event.get("ip_address"),
        "payment": event.get("payment_method_hash"),
        "address": event.get("shipping_address_hash"),
        "email": event.get("email_hash"),
        "phone": event.get("phone_hash"),
        "browser": event.get("browser_fingerprint"),
    }

    for key, value in entity_map.items():
        if not value:
            continue

        customer_entities[customer][key] = value

        if key == "device":
            device_index[value].add(customer)
        elif key == "ip":
            ip_index[value].add(customer)
        elif key == "payment":
            payment_index[value].add(customer)
        elif key == "address":
            address_index[value].add(customer)
        elif key == "email":
            email_index[value].add(customer)
        elif key == "phone":
            phone_index[value].add(customer)
        elif key == "browser":
            browser_index[value].add(customer)


# ==============================
# COMMUNITY DETECTION (CORE)
# ==============================


def detect_fraud_community(start_customer: str):

    if not LOG_FILE.exists():
        return None

    # Build graph from logs
    entity_to_customers = defaultdict(set)
    customer_to_entities = defaultdict(list)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)

            customer = r.get("customer_id")

            entity_map = {
                "device": r.get("device_id"),
                "ip": r.get("ip_address"),
                "payment": r.get("payment_method_hash"),
                "address": r.get("shipping_address_hash"),
                "email": r.get("email_hash"),
                "phone": r.get("phone_hash"),
                "browser": r.get("browser_fingerprint"),
            }

            for key, value in entity_map.items():
                if value:
                    entity_key = f"{key}:{value}"
                    entity_to_customers[entity_key].add(customer)
                    customer_to_entities[customer].append(entity_key)

    # BFS traversal
    visited = set()
    queue = deque([start_customer])

    while queue:
        customer = queue.popleft()

        if customer in visited:
            continue

        visited.add(customer)

        for entity in customer_to_entities.get(customer, []):
            for neighbor in entity_to_customers[entity]:
                if neighbor not in visited:
                    queue.append(neighbor)

    if len(visited) >= COMMUNITY_MIN_SIZE:
        return {
            "type": "FRAUD_NETWORK_COMMUNITY",
            "customers": list(visited),
            "community_size": len(visited)
        }

    return None