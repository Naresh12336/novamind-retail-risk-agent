import json
import os
from datetime import datetime

ALERT_FILE = "logs/high_risk_alerts.json"


def emit_alert(alert_data: dict):
    os.makedirs("logs", exist_ok=True)

    alert_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        **alert_data
    }

    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(alert_entry)

    with open(ALERT_FILE, "w") as f:
        json.dump(data, f, indent=4)
