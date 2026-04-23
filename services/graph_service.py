# graph_service.py

from collections import defaultdict, deque

# =====================================
# INDEXES
# =====================================
device_index = defaultdict(set)
ip_index = defaultdict(set)
payment_index = defaultdict(set)
address_index = defaultdict(set)
email_index = defaultdict(set)
phone_index = defaultdict(set)
browser_index = defaultdict(set)

customer_entities = defaultdict(list)

# =====================================
# THRESHOLDS
# =====================================
DEVICE_CLUSTER_THRESHOLD = 2
IP_CLUSTER_THRESHOLD = 2
PAYMENT_CLUSTER_THRESHOLD = 2
ADDRESS_CLUSTER_THRESHOLD = 2
EMAIL_CLUSTER_THRESHOLD = 2
PHONE_CLUSTER_THRESHOLD = 2
BROWSER_CLUSTER_THRESHOLD = 2

COMMUNITY_MIN_SIZE = 4


# =====================================
# HELPERS
# =====================================
def _add(index, entity_type, entity_value, customer):
    index[entity_value].add(customer)
    customer_entities[customer].append(f"{entity_type}:{entity_value}")


def _neighbors(entity_key: str):
    entity_type, entity_value = entity_key.split(":", 1)

    mapping = {
        "device": device_index,
        "ip": ip_index,
        "payment": payment_index,
        "address": address_index,
        "email": email_index,
        "phone": phone_index,
        "browser": browser_index
    }

    return mapping[entity_type][entity_value]


# =====================================
# UPDATE GRAPH
# =====================================
def update_graph(event: dict):

    customer = event.get("customer_id")

    if not customer:
        return

    entity_map = {
        "device": event.get("device_id"),
        "ip": event.get("ip_address"),
        "payment": event.get("payment_method_hash"),
        "address": event.get("shipping_address_hash"),
        "email": event.get("email_hash"),
        "phone": event.get("phone_hash"),
        "browser": event.get("browser_fingerprint"),
    }

    for entity_type, value in entity_map.items():
        if not value:
            continue

        if entity_type == "device":
            _add(device_index, entity_type, value, customer)
        elif entity_type == "ip":
            _add(ip_index, entity_type, value, customer)
        elif entity_type == "payment":
            _add(payment_index, entity_type, value, customer)
        elif entity_type == "address":
            _add(address_index, entity_type, value, customer)
        elif entity_type == "email":
            _add(email_index, entity_type, value, customer)
        elif entity_type == "phone":
            _add(phone_index, entity_type, value, customer)
        elif entity_type == "browser":
            _add(browser_index, entity_type, value, customer)


# =====================================
# DIRECT CLUSTERS
# =====================================
def detect_graph_cluster(event: dict):

    checks = [
        ("SHARED_DEVICE_CLUSTER", event.get("device_id"), device_index, DEVICE_CLUSTER_THRESHOLD),
        ("SHARED_IP_CLUSTER", event.get("ip_address"), ip_index, IP_CLUSTER_THRESHOLD),
        ("SHARED_PAYMENT_CLUSTER", event.get("payment_method_hash"), payment_index, PAYMENT_CLUSTER_THRESHOLD),
        ("SHARED_ADDRESS_CLUSTER", event.get("shipping_address_hash"), address_index, ADDRESS_CLUSTER_THRESHOLD),
        ("SHARED_EMAIL_CLUSTER", event.get("email_hash"), email_index, EMAIL_CLUSTER_THRESHOLD),
        ("SHARED_PHONE_CLUSTER", event.get("phone_hash"), phone_index, PHONE_CLUSTER_THRESHOLD),
        ("SHARED_BROWSER_CLUSTER", event.get("browser_fingerprint"), browser_index, BROWSER_CLUSTER_THRESHOLD),
    ]

    for cluster_type, entity, index, threshold in checks:
        if entity and len(index[entity]) >= threshold:
            return {
                "type": cluster_type,
                "entity": entity,
                "customers": list(index[entity]),
                "cluster_size": len(index[entity])
            }

    return None


# =====================================
# RISK SIGNAL
# =====================================
def get_graph_risk_signal(event: dict):

    cluster = detect_graph_cluster(event)

    if cluster:
        return cluster["type"].lower()

    return None


# =====================================
# COMMUNITY DETECTION
# =====================================
def detect_fraud_community(start_customer: str):

    if not start_customer:
        return None

    visited = set()
    queue = deque([start_customer])

    while queue:
        customer = queue.popleft()

        if customer in visited:
            continue

        visited.add(customer)

        for entity_key in customer_entities.get(customer, []):
            for neighbor in _neighbors(entity_key):
                if neighbor not in visited:
                    queue.append(neighbor)

    if len(visited) >= COMMUNITY_MIN_SIZE:
        return {
            "type": "FRAUD_NETWORK_COMMUNITY",
            "customers": list(visited),
            "community_size": len(visited)
        }

    return None