from threat_intelligence.ip_reputation import (
    update_ip_reputation
)

from threat_intelligence.email_reputation import (
    update_email_reputation
)

from threat_intelligence.device_reputation import (
    update_device_reputation
)


# ==========================================
# UPDATE ALL REPUTATION STORES
# ==========================================
def update_threat_intelligence(
    event,
    result
):

    update_ip_reputation(

        event.get(
            "ip_address"
        ),

        event.get(
            "customer_id"
        ),

        result
    )

    update_email_reputation(

        event.get(
            "email_hash"
        ),

        event.get(
            "customer_id"
        ),

        result
    )

    update_device_reputation(

        event.get(
            "device_id"
        ),

        event.get(
            "customer_id"
        ),

        result
    )