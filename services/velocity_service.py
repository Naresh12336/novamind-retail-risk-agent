from collections import defaultdict, deque
from datetime import datetime, timedelta

# ==========================================
# IN-MEMORY EVENT WINDOWS
# ==========================================
ip_events = defaultdict(deque)
device_events = defaultdict(deque)
payment_events = defaultdict(deque)

# ==========================================
# THRESHOLDS
# ==========================================
WINDOW_MINUTES = 10

IP_BURST_THRESHOLD = 5
DEVICE_BURST_THRESHOLD = 4
PAYMENT_BURST_THRESHOLD = 4


# ==========================================
# HELPERS
# ==========================================
def now():
    return datetime.utcnow()


def cutoff():
    return now() - timedelta(minutes=WINDOW_MINUTES)


def clean_old(queue_obj):
    limit = cutoff()

    while queue_obj and queue_obj[0] < limit:
        queue_obj.popleft()


# ==========================================
# UPDATE WINDOWS
# ==========================================
def update_velocity(event: dict):

    ts = now()

    ip = event.get("ip_address")
    device = event.get("device_id")
    payment = event.get("payment_method_hash")

    if ip:
        ip_events[ip].append(ts)
        clean_old(ip_events[ip])

    if device:
        device_events[device].append(ts)
        clean_old(device_events[device])

    if payment:
        payment_events[payment].append(ts)
        clean_old(payment_events[payment])


# ==========================================
# DETECTION
# ==========================================
def detect_velocity_cluster(event: dict):

    findings = []

    ip = event.get("ip_address")
    device = event.get("device_id")
    payment = event.get("payment_method_hash")

    if ip:
        clean_old(ip_events[ip])

        if len(ip_events[ip]) >= IP_BURST_THRESHOLD:
            findings.append({
                "type": "IP_VELOCITY_CLUSTER",
                "entity": ip,
                "count": len(ip_events[ip]),
                "window_minutes": WINDOW_MINUTES,
                "severity": "High"
            })

    if device:
        clean_old(device_events[device])

        if len(device_events[device]) >= DEVICE_BURST_THRESHOLD:
            findings.append({
                "type": "DEVICE_VELOCITY_CLUSTER",
                "entity": device,
                "count": len(device_events[device]),
                "window_minutes": WINDOW_MINUTES,
                "severity": "High"
            })

    if payment:
        clean_old(payment_events[payment])

        if len(payment_events[payment]) >= PAYMENT_BURST_THRESHOLD:
            findings.append({
                "type": "PAYMENT_VELOCITY_CLUSTER",
                "entity": payment,
                "count": len(payment_events[payment]),
                "window_minutes": WINDOW_MINUTES,
                "severity": "High"
            })

    return findings