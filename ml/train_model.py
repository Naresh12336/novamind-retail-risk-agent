import pandas as pd
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

from xgboost import XGBClassifier

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = (
    BASE_DIR / "ml" / "fraud_dataset.csv"
)

MODEL_PATH = (
    BASE_DIR / "ml" / "xgboost_fraud_model.pkl"
)


# ==========================================
# LOAD DATASET
# ==========================================
df = pd.read_csv(DATASET_PATH)

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMNS:")
print(df.columns.tolist())

# ==========================================
# TARGET LABEL
# ==========================================
TARGET_COLUMN = "was_blocked"

# ==========================================
# FEATURES / LABELS
# ==========================================
DROP_COLUMNS = [
    "was_blocked",
    "is_high_risk",

    # remove aggregated scores
    "risk_score",
    "graph_score",
    "velocity_score",
    "ato_score",
    "geo_score",
    "asn_score"
]

X = df.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)

y = df[TARGET_COLUMN]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# XGBOOST MODEL
# ==========================================
model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42
)

# ==========================================
# TRAIN
# ==========================================
print("\nTRAINING MODEL...\n")

model.fit(X_train, y_train)

# ==========================================
# PREDICT
# ==========================================
y_pred = model.predict(X_test)

# ==========================================
# METRICS
# ==========================================
print("\nACCURACY:")
print(
    accuracy_score(y_test, y_pred)
)

print("\nCONFUSION MATRIX:")
print(
    confusion_matrix(y_test, y_pred)
)

print("\nCLASSIFICATION REPORT:")
print(
    classification_report(y_test, y_pred)
)

# ==========================================
# FEATURE IMPORTANCE
# ==========================================
importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nTOP FEATURE IMPORTANCE:\n")
print(
    importance_df.head(15)
)

# ==========================================
# SAVE MODEL
# ==========================================
joblib.dump(
    model,
    MODEL_PATH
)

print(
    f"\nMODEL SAVED: {MODEL_PATH}"
)