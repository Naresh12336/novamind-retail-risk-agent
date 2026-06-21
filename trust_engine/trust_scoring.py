from trust_engine.trust_store import (
    trust_scores
)


# ==========================================
# GET TRUST SCORE
# ==========================================
def get_trust_score(
    entity_id
):

    return trust_scores.get(
        entity_id,
        50
    )


# ==========================================
# ADJUST TRUST SCORE
# ==========================================
def adjust_trust_score(
    entity_id,
    delta
):

    current = trust_scores[
        entity_id
    ]

    updated = max(
        0,
        min(
            100,
            current + delta
        )
    )

    trust_scores[
        entity_id
    ] = updated

    return updated