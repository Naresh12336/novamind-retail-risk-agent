from pathlib import Path

import pandas as pd

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    BASE_DIR / "ml" / "fraud_dataset.csv"
)


# ==========================================
# DATASET WRITER
# ==========================================
def append_training_sample(
    features: dict
):

    try:

        if not features:

            return

        required_columns = {

            "risk_score",

            "keyword_count",

            "amount",

            "graph_score",

            "velocity_score",

            "ato_score",

            "geo_score",

            "asn_score",

            "threat_score",

            "trust_score",

            "merchant_score"

        }

        missing = required_columns - set(features.keys())

        if missing:
            raise ValueError(
                f"Missing dataset features: {sorted(missing)}"
            )

        row = pd.DataFrame(
            [features]
        )

        DATASET_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_exists = (
            DATASET_FILE.exists()
        )

        row.to_csv(

            DATASET_FILE,

            mode="a" if file_exists else "w",

            header=not file_exists,

            index=False

        )

    except Exception as e:

        print(

            "DATASET WRITER ERROR:",

            str(e)

        )