from collections import defaultdict

# entity indexes
device_index = defaultdict(set)
ip_index = defaultdict(set)
payment_index = defaultdict(set)
address_index = defaultdict(set)

# thresholds for fraud clusters
DEVICE_CLUSTER_THRESHOLD = 4
IP_CLUSTER_THRESHOLD = 5
PAYMENT_CLUSTER_THRESHOLD = 3
ADDRESS_CLUSTER_THRESHOLD = 3


def update_graph(event: dict):
    """
    Update entity indexes with the latest transaction event.
    """

    customer = event.get("customer_id")

    device = event.get("device_id")
    ip = event.get("ip_address")
    payment = event.get("payment_method_hash")
    address = event.get("shipping_address_hash")

    if device:
        device_index[device].add(customer)

    if ip:
        ip_index[ip].add(customer)

    if payment:
        payment_index[payment].add(customer)

    if address:
        address_index[address].add(customer)


def detect_graph_cluster(event: dict):
    """
    Detect shared infrastructure fraud clusters.
    """

    customer = event.get("customer_id")

    device = event.get("device_id")
    ip = event.get("ip_address")
    payment = event.get("payment_method_hash")
    address = event.get("shipping_address_hash")

    # device cluster detection
    if device and len(device_index[device]) >= DEVICE_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_DEVICE_CLUSTER",
            "entity": device,
            "customers": list(device_index[device]),
            "cluster_size": len(device_index[device])
        }

    # ip cluster detection
    if ip and len(ip_index[ip]) >= IP_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_IP_CLUSTER",
            "entity": ip,
            "customers": list(ip_index[ip]),
            "cluster_size": len(ip_index[ip])
        }

    # payment method cluster detection
    if payment and len(payment_index[payment]) >= PAYMENT_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_PAYMENT_CLUSTER",
            "entity": payment,
            "customers": list(payment_index[payment]),
            "cluster_size": len(payment_index[payment])
        }

    # shipping address cluster detection
    if address and len(address_index[address]) >= ADDRESS_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_ADDRESS_CLUSTER",
            "entity": address,
            "customers": list(address_index[address]),
            "cluster_size": len(address_index[address])
        }

    return None