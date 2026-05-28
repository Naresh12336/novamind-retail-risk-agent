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

model = joblib.load(MODEL_PATH)

# ==========================================
# SHAP EXPLAINER
# ==========================================
explainer = shap.TreeExplainer(model)

# ==========================================
# MAIN EXPLAINABILITY
# ==========================================
def explain_prediction(features: dict):

    try:

        # ----------------------------------
        # DATAFRAME
        # ----------------------------------
        X = pd.DataFrame([features])

        # ----------------------------------
        # SHAP VALUES
        # ----------------------------------
        shap_values = explainer.shap_values(X)

        contributions = []

        # ----------------------------------
        # FEATURE IMPACTS
        # ----------------------------------
        for idx, feature_name in enumerate(X.columns):

            impact = float(
                shap_values[0][idx]
            )

            contributions.append({
                "feature": feature_name,
                "impact": round(impact, 4),
                "value": X.iloc[0][feature_name]
            })

        # ----------------------------------
        # SORT BY ABSOLUTE IMPACT
        # ----------------------------------
        contributions = sorted(
            contributions,
            key=lambda x: abs(x["impact"]),
            reverse=True
        )

        # ----------------------------------
        # TOP CONTRIBUTORS
        # ----------------------------------
        top_contributors = contributions[:5]

        return {
            "top_contributors":
                top_contributors,

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