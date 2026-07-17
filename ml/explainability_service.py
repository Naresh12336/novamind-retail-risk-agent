import shap
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
explainer = None

if MODEL_PATH.exists():

    try:

        model = joblib.load(
            MODEL_PATH
        )

        explainer = shap.TreeExplainer(
            model
        )

        print(
            "SHAP explainer loaded."
        )

    except Exception as e:

        print(
            "Failed to load SHAP model:",
            str(e)
        )

else:

    print(
        "SHAP disabled. ML model not found."
    )


# ==========================================
# MAIN EXPLAINABILITY
# ==========================================
def explain_prediction(
    features: dict
):

    # ----------------------------------
    # RULE-ONLY MODE
    # ----------------------------------
    if (
        model is None
        or
        explainer is None
    ):

        return {

            "top_contributors": [],

            "all_contributions": []

        }

    try:

        # ----------------------------------
        # DATAFRAME
        # ----------------------------------
        X = pd.DataFrame(
            [features]
        )

        # ----------------------------------
        # SHAP VALUES
        # ----------------------------------
        shap_values = explainer.shap_values(
            X
        )

        # ----------------------------------
        # XGBOOST BINARY OUTPUT
        # ----------------------------------
        if isinstance(
            shap_values,
            list
        ):

            shap_values = shap_values[1]

        contributions = []

        # ----------------------------------
        # FEATURE CONTRIBUTIONS
        # ----------------------------------
        for idx, feature_name in enumerate(
            X.columns
        ):

            impact = float(
                shap_values[0][idx]
            )

            contributions.append({

                "feature": feature_name,

                "impact": round(
                    impact,
                    4
                ),

                "value": X.iloc[
                    0
                ][
                    feature_name
                ]

            })

        # ----------------------------------
        # SORT
        # ----------------------------------
        contributions.sort(

            key=lambda item: abs(
                item["impact"]
            ),

            reverse=True

        )

        return {

            "top_contributors":
                contributions[:5],

            "all_contributions":
                contributions

        }

    except Exception as e:

        print(
            "SHAP EXPLAIN ERROR:",
            str(e)
        )

        return {

            "top_contributors": [],

            "all_contributions": []

        }