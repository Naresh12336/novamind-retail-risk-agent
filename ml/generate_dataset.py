import json
from pathlib import Path

import pandas as pd

from ml.feature_builder import (
    build_feature_vector
)

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE = (
    BASE_DIR / "logs" / "decision_history.jsonl"
)

OUTPUT_FILE = (
    BASE_DIR / "ml" / "fraud_dataset.csv"
)


# ==========================================
# MAIN
# ==========================================
def generate_dataset():

    if not LOG_FILE.exists():

        print(
            "decision_history.jsonl not found."
        )

        return

    rows = []

    with open(
        LOG_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            try:

                record = json.loads(line)

                # ----------------------------------
                # EVENT
                # ----------------------------------
                event = {

                    "amount":
                        record.get(
                            "amount",
                            0
                        ),

                    "refund_count_last_30_days":
                        record.get(
                            "refund_count_last_30_days",
                            0
                        ),

                    "account_age_days":
                        record.get(
                            "account_age_days",
                            0
                        )
                }

                # ----------------------------------
                # RESULT
                # ----------------------------------
                partial_result = {

                    # Risk
                    "risk_score":
                        record.get(
                            "risk_score",
                            0
                        ),

                    "risk_category":
                        record.get(
                            "risk_category"
                        ),

                    "recommended_action":
                        record.get(
                            "action"
                        ),

                    # Infrastructure Scores
                    "graph_score":
                        record.get(
                            "graph_score",
                            0
                        ),

                    "velocity_score":
                        record.get(
                            "velocity_score",
                            0
                        ),

                    "ato_score":
                        record.get(
                            "ato_score",
                            0
                        ),

                    "geo_score":
                        record.get(
                            "geo_score",
                            0
                        ),

                    "asn_score":
                        record.get(
                            "asn_score",
                            0
                        ),

                    "threat_score":
                        record.get(
                            "threat_score",
                            0
                        ),

                    "trust_score":
                        record.get(
                            "trust_score",
                            0
                        ),

                    "merchant_score":
                        record.get(
                            "merchant_score",
                            0
                        ),

                    # Signals
                    "graph_signals":
                        record.get(
                            "graph_signals",
                            []
                        ),

                    "velocity_clusters":
                        record.get(
                            "velocity_clusters",
                            []
                        ),

                    "ato_findings":
                        record.get(
                            "ato_findings",
                            []
                        ),

                    "geo_signals":
                        record.get(
                            "geo_signals",
                            []
                        ),

                    "asn_signals":
                        record.get(
                            "asn_signals",
                            []
                        ),

                    "threat_signals":
                        record.get(
                            "threat_signals",
                            []
                        ),

                    "trust_signals":
                        record.get(
                            "trust_signals",
                            []
                        ),

                    "merchant_signals":
                        record.get(
                            "merchant_signals",
                            []
                        ),

                    # Reputation
                    "reputation_before":
                        record.get(
                            "reputation_before",
                            50
                        ),

                    # Evidence
                    "evidence": {

                        "textual_signals": {

                            "keyword_count":
                                record.get(
                                    "keyword_count",
                                    0
                                ),

                            "urgency_flag":
                                record.get(
                                    "urgency_flag",
                                    False
                                ),

                            "text_length":
                                record.get(
                                    "text_length",
                                    0
                                )

                        },

                        "behavioral_signals": {

                            "amount":
                                record.get(
                                    "amount",
                                    0
                                ),

                            "refund_count_last_30_days":
                                record.get(
                                    "refund_count_last_30_days",
                                    0
                                ),

                            "account_age_days":
                                record.get(
                                    "account_age_days",
                                    0
                                )

                        },

                        "honeypot_signals": {

                            "tactic_count":
                                record.get(
                                    "tactic_count",
                                    0
                                )

                        }

                    }

                }

                features = build_feature_vector(
                    event=event,
                    partial_result= partial_result,
                )

                rows.append(
                    features
                )

            except Exception as e:

                print(
                    "DATASET ERROR:",
                    str(e)
                )

    if not rows:

        print(
            "No dataset rows generated."
        )

        return

    df = pd.DataFrame(rows)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Dataset generated: {OUTPUT_FILE}"
    )

    print(
        "\nDataset Shape:"
    )

    print(
        df.shape
    )

    print(
        "\nColumns:"
    )

    print(
        list(df.columns)
    )

    print(
        "\nPreview:"
    )

    print(
        df.head()
    )


# ==========================================
# ENTRYPOINT
# ==========================================
if __name__ == "__main__":

    generate_dataset()