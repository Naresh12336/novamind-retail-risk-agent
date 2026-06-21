from trust_engine.trust_scoring import (
    adjust_trust_score
)

from trust_engine.trust_propagation import (
    propagate_trust_penalty
)

# ==========================================
# UPDATE ENTITY TRUST
# ==========================================
def update_entity_trust(
    event,
    result
):

    risk_category = result.get(
        "risk_category"
    )

    action = result.get(
        "recommended_action"
    )

    customer = (
        f"customer:"
        f"{event.get('customer_id')}"
    )

    ip = (
        f"ip:"
        f"{event.get('ip_address')}"
    )

    device = (
        f"device:"
        f"{event.get('device_id')}"
    )

    email = (
        f"email:"
        f"{event.get('email_hash')}"
    )

    entities = [
        customer,
        ip,
        device,
        email
    ]

    # ==========================
    # FRAUD
    # ==========================
    if action == (
        "Auto Block Transaction"
    ):

        delta = -15

    elif risk_category == "High":

        delta = -10

    elif risk_category == "Medium":

        delta = -3

    else:

        delta = 1

    for entity in entities:

        adjust_trust_score(
            entity,
            delta
        )
    if action == (
            "Auto Block Transaction"
    ):
        linked = (
            propagate_trust_penalty(
                event.get(
                    "customer_id"
                ),
                severity=8
            )
        )

        print(
            "TRUST PROPAGATION:",
            linked
        )