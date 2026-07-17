import joblib
import pandas as pd

from pathlib import Path

# ==========================================
# LOAD MODEL
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR / "ml" / "xgboost_fraud_model.pkl"
)

model = None

if MODEL_PATH.exists():

    try:

        model = joblib.load(
            MODEL_PATH
        )

        print(
            "ML model loaded."
        )

    except Exception as e:

        print(
            "Failed to load ML model:",
            str(e)
        )

else:

    print(
        "ML model not found. Running in rule-only mode."
    )


# ==========================================
# TRAINING LABELS
# ==========================================
DROP_COLUMNS = [

    "was_blocked",

    "is_high_risk",

    "risk_score"
]


# ==========================================
# MAIN INFERENCE
# ==========================================
def predict_fraud_risk(
    features: dict
):

    if model is None:

        return {

            "prediction": 0,

            "fraud_probability": 0.0,

            "features": features

        }

    try:

        # ----------------------------------
        # COPY FEATURES
        # ----------------------------------
        model_features = features.copy()

        # ----------------------------------
        # REMOVE TRAINING LABELS
        # ----------------------------------
        for column in DROP_COLUMNS:

            model_features.pop(
                column,
                None
            )

        # ----------------------------------
        # DATAFRAME
        # ----------------------------------
        x = pd.DataFrame(
            [model_features]
        )

        # ----------------------------------
        # PREDICTION
        # ----------------------------------
        prediction = model.predict(
            x
        )[0]

        probability = model.predict_proba(
            x
        )[0][1]

        # ----------------------------------
        # RESULT
        # ----------------------------------
        return {

            "prediction": int(
                prediction
            ),

            "fraud_probability": round(
                float(probability),
                4
            ),

            "features": model_features

        }

    except Exception as e:

        print(
            "ML INFERENCE ERROR:",
            str(e)
        )

        return {

            "prediction": 0,

            "fraud_probability": 0.0,

            "features": features

        }