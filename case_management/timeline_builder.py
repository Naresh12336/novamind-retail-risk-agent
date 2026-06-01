from analytics.decision_logger import (
    get_customer_history
)


# ==========================================
# CUSTOMER TIMELINE
# ==========================================
def build_customer_timeline(
    customer_id
):

    events = get_customer_history(
        customer_id
    )

    timeline = []

    for event in events:

        timeline.append({

            "timestamp":
                event.get(
                    "timestamp"
                ),

            "transaction_id":
                event.get(
                    "transaction_id"
                ),

            "risk_score":
                event.get(
                    "risk_score"
                ),

            "risk_category":
                event.get(
                    "risk_category"
                ),

            "action":
                event.get(
                    "action"
                ),

            "graph_score":
                event.get(
                    "graph_score",
                    0
                ),

            "geo_score":
                event.get(
                    "geo_score",
                    0
                ),

            "asn_score":
                event.get(
                    "asn_score",
                    0
                )
        })

    return sorted(
        timeline,
        key=lambda x:
            x["timestamp"]
    )