# services/graph_service.py

from collections import defaultdict, deque

# ==================================================
# IN-MEMORY ENTITY INDEXES
# ==================================================
device_index = defaultdict(set)
ip_index = defaultdict(set)
payment_index = defaultdict(set)
address_index = defaultdict(set)
email_index = defaultdict(set)
phone_index = defaultdict(set)
browser_index = defaultdict(set)

# customer -> linked entities
customer_entities = defaultdict(set)

# ==================================================
# THRESHOLDS
# ==================================================
DEVICE_CLUSTER_THRESHOLD = 2
IP_CLUSTER_THRESHOLD = 2
PAYMENT_CLUSTER_THRESHOLD = 2
ADDRESS_CLUSTER_THRESHOLD = 2
EMAIL_CLUSTER_THRESHOLD = 2
PHONE_CLUSTER_THRESHOLD = 2
BROWSER_CLUSTER_THRESHOLD = 2

COMMUNITY_MIN_SIZE = 4

# ==================================================
# WEIGHTED RISK SCORES
# ==================================================
GRAPH_WEIGHTS = {
    "shared_payment_cluster": 35,
    "shared_device_cluster": 25,
    "shared_phone_cluster": 20,
    "shared_browser_cluster": 18,
    "shared_email_cluster": 15,
    "shared_address_cluster": 12,
    "shared_ip_cluster": 10,
    "fraud_network_community": 40
}

# ==================================================
# ENTITY LOOKUP MAP
# ==================================================
ENTITY_LOOKUP = {
    "device": device_index,
    "ip": ip_index,
    "payment": payment_index,
    "address": address_index,
    "email": email_index,
    "phone": phone_index,
    "browser": browser_index
}


# ==================================================
# INTERNAL HELPERS
# ==================================================
def _add_entity(index, customer_id, entity_type, entity_value):
    if not entity_value:
        return

    index[entity_value].add(customer_id)
    customer_entities[customer_id].add(f"{entity_type}:{entity_value}")


def _cluster_payload(cluster_type, entity, customers):
    return {
        "type": cluster_type,
        "entity": entity,
        "customers": list(customers),
        "cluster_size": len(customers)
    }


# ==================================================
# GRAPH UPDATE
# ==================================================
def update_graph(event: dict):

    customer_id = event.get("customer_id")

    if not customer_id:
        return

    _add_entity(device_index, customer_id, "device", event.get("device_id"))
    _add_entity(ip_index, customer_id, "ip", event.get("ip_address"))
    _add_entity(payment_index, customer_id, "payment", event.get("payment_method_hash"))
    _add_entity(address_index, customer_id, "address", event.get("shipping_address_hash"))
    _add_entity(email_index, customer_id, "email", event.get("email_hash"))
    _add_entity(phone_index, customer_id, "phone", event.get("phone_hash"))
    _add_entity(browser_index, customer_id, "browser", event.get("browser_fingerprint"))


# ==================================================
# DIRECT CLUSTER DETECTION
# ==================================================
def detect_graph_cluster(event: dict):

    clusters = []

    try:
        device = event.get("device_id")
        ip = event.get("ip_address")
        payment = event.get("payment_method_hash")
        address = event.get("shipping_address_hash")
        email = event.get("email_hash")
        phone = event.get("phone_hash")
        browser = event.get("browser_fingerprint")

        if device and len(device_index[device]) >= DEVICE_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_device_cluster",
                    device,
                    device_index[device]
                )
            )

        if ip and len(ip_index[ip]) >= IP_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_ip_cluster",
                    ip,
                    ip_index[ip]
                )
            )

        if payment and len(payment_index[payment]) >= PAYMENT_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_payment_cluster",
                    payment,
                    payment_index[payment]
                )
            )

        if address and len(address_index[address]) >= ADDRESS_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_address_cluster",
                    address,
                    address_index[address]
                )
            )

        if email and len(email_index[email]) >= EMAIL_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_email_cluster",
                    email,
                    email_index[email]
                )
            )

        if phone and len(phone_index[phone]) >= PHONE_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_phone_cluster",
                    phone,
                    phone_index[phone]
                )
            )

        if browser and len(browser_index[browser]) >= BROWSER_CLUSTER_THRESHOLD:
            clusters.append(
                _cluster_payload(
                    "shared_browser_cluster",
                    browser,
                    browser_index[browser]
                )
            )

    except Exception as e:
        print("GRAPH CLUSTER ERROR:", str(e))
        return []

    return clusters


# ==================================================
# COMMUNITY DETECTION
# ==================================================
def detect_fraud_community(start_customer: str):

    if not start_customer:
        return None

    try:
        visited = set()
        queue = deque([start_customer])

        while queue:
            customer = queue.popleft()

            if customer in visited:
                continue

            visited.add(customer)

            for entity_key in customer_entities.get(customer, set()):

                if ":" not in entity_key:
                    continue

                entity_type, entity_value = entity_key.split(":", 1)

                if entity_type not in ENTITY_LOOKUP:
                    continue

                neighbors = ENTITY_LOOKUP[entity_type].get(entity_value, set())

                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append(neighbor)

        if len(visited) >= COMMUNITY_MIN_SIZE:
            return {
                "type": "fraud_network_community",
                "customers": list(visited),
                "community_size": len(visited)
            }

    except Exception as e:
        print("GRAPH COMMUNITY ERROR:", str(e))
        return None

    return None


# ==================================================
# WEIGHTED GRAPH SCORING
# ==================================================
def get_graph_risk_score(event: dict):

    signals = []
    total_score = 0

    clusters = detect_graph_cluster(event)

    if not isinstance(clusters, list):
        clusters = []

    for cluster in clusters:

        if not isinstance(cluster, dict):
            continue

        signal = cluster.get("type")

        if signal and signal in GRAPH_WEIGHTS:
            signals.append(signal)
            total_score += GRAPH_WEIGHTS[signal]

    community = detect_fraud_community(event.get("customer_id"))

    if community:
        signals.append("fraud_network_community")
        total_score += GRAPH_WEIGHTS["fraud_network_community"]

    return {
        "signals": signals,
        "score": total_score,
        "clusters": clusters,
        "community": community
    }


# ==================================================
# BACKWARD COMPATIBILITY
# ==================================================
def get_graph_risk_signal(event: dict):

    result = get_graph_risk_score(event)

    if result["signals"]:
        return result["signals"][0]

    return None