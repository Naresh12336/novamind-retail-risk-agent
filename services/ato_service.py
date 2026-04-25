from collections import defaultdict, deque
from datetime import datetime, timedelta

# ==========================================
# ACCOUNT HISTORY WINDOWS
# ==========================================
account_ip_history = defaultdict(deque)
account_device_history = defaultdict(deque)
account_browser_history = defaultdict(deque)

WINDOW_MINUTES = 15

IP_ROTATION_THRESHOLD = 3
DEVICE_ROTATION_THRESHOLD = 3
BROWSER_MUTATION_THRESHOLD = 3


# ==========================================
# HELPERS
# ==========================================
def now():
    return datetime.utcnow()


def cutoff():
    return now() - timedelta(minutes=WINDOW_MINUTES)


def clean_old(queue_obj):
    limit = cutoff()

    while queue_obj and queue_obj[0][0] < limit:
        queue_obj.popleft()


# ==========================================
# UPDATE ACCOUNT HISTORY
# ==========================================
def update_account_behavior(event: dict):

    customer = event.get("customer_id")

    if not customer:
        return

    ts = now()

    ip = event.get("ip_address")
    device = event.get("device_id")
    browser = event.get("browser_fingerprint")

    if ip:
        account_ip_history[customer].append((ts, ip))
        clean_old(account_ip_history[customer])

    if device:
        account_device_history[customer].append((ts, device))
        clean_old(account_device_history[customer])

    if browser:
        account_browser_history[customer].append((ts, browser))
        clean_old(account_browser_history[customer])


# ==========================================
# DETECT ACCOUNT TAKEOVER
# ==========================================
def detect_account_takeover(event: dict):

    customer = event.get("customer_id")

    if not customer:
        return []

    findings = []

    # IP rotation
    ips = {x[1] for x in account_ip_history[customer]}
    if len(ips) >= IP_ROTATION_THRESHOLD:
        findings.append({
            "type": "ACCOUNT_IP_ROTATION",
            "customer_id": customer,
            "count": len(ips),
            "window_minutes": WINDOW_MINUTES,
            "severity": "High"
        })

    # Device rotation
    devices = {x[1] for x in account_device_history[customer]}
    if len(devices) >= DEVICE_ROTATION_THRESHOLD:
        findings.append({
            "type": "ACCOUNT_DEVICE_ROTATION",
            "customer_id": customer,
            "count": len(devices),
            "window_minutes": WINDOW_MINUTES,
            "severity": "High"
        })

    # Browser mutation
    browsers = {x[1] for x in account_browser_history[customer]}
    if len(browsers) >= BROWSER_MUTATION_THRESHOLD:
        findings.append({
            "type": "ACCOUNT_BROWSER_MUTATION",
            "customer_id": customer,
            "count": len(browsers),
            "window_minutes": WINDOW_MINUTES,
            "severity": "Medium"
        })

    if len(findings) >= 2:
        findings.append({
            "type": "ACCOUNT_TAKEOVER_RISK",
            "customer_id": customer,
            "severity": "Critical"
        })

    return findings