from collections import defaultdict

# entity indexes
device_index = defaultdict(set)
ip_index = defaultdict(set)
payment_index = defaultdict(set)
address_index = defaultdict(set)
email_index = defaultdict(set)
phone_index = defaultdict(set)
browser_index = defaultdict(set)

# thresholds for fraud clusters
DEVICE_CLUSTER_THRESHOLD = 4
IP_CLUSTER_THRESHOLD = 5
PAYMENT_CLUSTER_THRESHOLD = 3
ADDRESS_CLUSTER_THRESHOLD = 3
EMAIL_CLUSTER_THRESHOLD = 3
PHONE_CLUSTER_THRESHOLD = 3
BROWSER_CLUSTER_THRESHOLD = 4


def update_graph(event: dict):
    """
    Update entity indexes with the latest transaction event.
    """

    customer = event.get("customer_id")

    device = event.get("device_id")
    ip = event.get("ip_address")
    payment = event.get("payment_method_hash")
    address = event.get("shipping_address_hash")
    email = event.get("email_hash")
    phone = event.get("phone_hash")
    browser = event.get("browser_fingerprint")

    if device:
        device_index[device].add(customer)

    if ip:
        ip_index[ip].add(customer)

    if payment:
        payment_index[payment].add(customer)

    if address:
        address_index[address].add(customer)

    if email:
        email_index[email].add(customer)

    if phone:
        phone_index[phone].add(customer)

    if browser:
        browser_index[browser].add(customer)


def detect_graph_cluster(event: dict):
    """
    Detect shared infrastructure fraud clusters.
    """

    device = event.get("device_id")
    ip = event.get("ip_address")
    payment = event.get("payment_method_hash")
    address = event.get("shipping_address_hash")
    email = event.get("email_hash")
    phone = event.get("phone_hash")
    browser = event.get("browser_fingerprint")

    if device and len(device_index[device]) >= DEVICE_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_DEVICE_CLUSTER",
            "entity": device,
            "customers": list(device_index[device]),
            "cluster_size": len(device_index[device])
        }

    if ip and len(ip_index[ip]) >= IP_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_IP_CLUSTER",
            "entity": ip,
            "customers": list(ip_index[ip]),
            "cluster_size": len(ip_index[ip])
        }

    if payment and len(payment_index[payment]) >= PAYMENT_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_PAYMENT_CLUSTER",
            "entity": payment,
            "customers": list(payment_index[payment]),
            "cluster_size": len(payment_index[payment])
        }

    if address and len(address_index[address]) >= ADDRESS_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_ADDRESS_CLUSTER",
            "entity": address,
            "customers": list(address_index[address]),
            "cluster_size": len(address_index[address])
        }

    if email and len(email_index[email]) >= EMAIL_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_EMAIL_CLUSTER",
            "entity": email,
            "customers": list(email_index[email]),
            "cluster_size": len(email_index[email])
        }

    if phone and len(phone_index[phone]) >= PHONE_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_PHONE_CLUSTER",
            "entity": phone,
            "customers": list(phone_index[phone]),
            "cluster_size": len(phone_index[phone])
        }

    if browser and len(browser_index[browser]) >= BROWSER_CLUSTER_THRESHOLD:
        return {
            "type": "SHARED_BROWSER_CLUSTER",
            "entity": browser,
            "customers": list(browser_index[browser]),
            "cluster_size": len(browser_index[browser])
        }

    return None


def get_graph_risk_signal(event: dict):

    device = event.get("device_id")
    ip = event.get("ip_address")
    payment = event.get("payment_method_hash")

    if device and len(device_index[device]) >= DEVICE_CLUSTER_THRESHOLD:
        return "shared_device_cluster"

    if ip and len(ip_index[ip]) >= IP_CLUSTER_THRESHOLD:
        return "shared_ip_cluster"

    if payment and len(payment_index[payment]) >= PAYMENT_CLUSTER_THRESHOLD:
        return "shared_payment_cluster"

    return None