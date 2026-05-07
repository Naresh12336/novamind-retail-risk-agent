import joblib
import pandas as pd

from pathlib import Path

from ml.feature_builder import (
    build_feature_vector
)

# ==========================================
# LOAD MODEL
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR / "ml" / "xgboost_fraud_model.pkl"
)

model = joblib.load(MODEL_PATH)

# ==========================================
# DROPPED TRAINING COLUMNS
# ==========================================
DROP_COLUMNS = [
    "was_blocked",
    "is_high_risk",

    "risk_score",
    "graph_score",
    "velocity_score",
    "ato_score",
    "geo_score",
    "asn_score"
]

# ==========================================
# MAIN INFERENCE
# ==========================================
def predict_fraud_risk(
    event: dict,
    result: dict
):

    try:

        # ----------------------------------
        # BUILD FEATURES
        # ----------------------------------
        features = build_feature_vector(
            event=event,
            result=result
        )

        # ----------------------------------
        # REMOVE TRAINING LABELS
        # ----------------------------------
        for col in DROP_COLUMNS:
            features.pop(col, None)

        # ----------------------------------
        # DATAFRAME
        # ----------------------------------
        X = pd.DataFrame([features])

        # ----------------------------------
        # PREDICTION
        # ----------------------------------
        prediction = model.predict(X)[0]

        probability = (
            model.predict_proba(X)[0][1]
        )

        return {
            "prediction": int(prediction),

            "fraud_probability": round(
                float(probability),
                4
            ),

            "features": features
        }

    except Exception as e:

        print(
            "ML INFERENCE ERROR:",
            str(e)
        )

        return {
            "prediction": 0,
            "fraud_probability": 0.0,
            "features": {}
        }