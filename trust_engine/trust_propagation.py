from trust_engine.trust_scoring import (
    adjust_trust_score
)

from services.graph_service import (
    customer_entities,
    ENTITY_LOOKUP
)


# ==========================================
# PROPAGATE TRUST PENALTY
# ==========================================
def propagate_trust_penalty(
    customer_id,
    severity=10
):

    if not customer_id:
        return []

    affected_customers = set()

    entities = customer_entities.get(
        customer_id,
        set()
    )

    for entity_key in entities:

        if ":" not in entity_key:
            continue

        entity_type, entity_value = (
            entity_key.split(
                ":",
                1
            )
        )

        lookup = ENTITY_LOOKUP.get(
            entity_type
        )

        if not lookup:
            continue

        linked_customers = lookup.get(
            entity_value,
            set()
        )

        for linked_customer in linked_customers:

            if linked_customer == customer_id:
                continue

            affected_customers.add(
                linked_customer
            )

    # ==========================
    # APPLY PENALTY
    # ==========================
    for linked_customer in affected_customers:

        adjust_trust_score(

            f"customer:{linked_customer}",

            -severity
        )

    return list(
        affected_customers
    )