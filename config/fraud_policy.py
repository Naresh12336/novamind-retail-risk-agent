# ==========================================
# DECISION POLICY
# ==========================================

AUTO_BLOCK_SCORE = 90

STEP_UP_SCORE = 50

CUSTOMER_VERIFICATION_SCORE = 45


# ==========================================
# ML DECISION POLICY
# ==========================================

ML_REVIEW_THRESHOLD = 0.90

ML_AUTO_BLOCK_THRESHOLD = 0.98

ML_LOW_CONFIDENCE_THRESHOLD = 0.20


# ==========================================
# INFRASTRUCTURE POLICY
# ==========================================

INFRA_REVIEW_THRESHOLD = 40

INFRA_AUTO_BLOCK_THRESHOLD = 60


# ==========================================
# GRAPH INTELLIGENCE
# ==========================================

DEVICE_CLUSTER_THRESHOLD = 2

IP_CLUSTER_THRESHOLD = 2

PAYMENT_CLUSTER_THRESHOLD = 2

ADDRESS_CLUSTER_THRESHOLD = 2

EMAIL_CLUSTER_THRESHOLD = 2

PHONE_CLUSTER_THRESHOLD = 2

BROWSER_CLUSTER_THRESHOLD = 2

COMMUNITY_MIN_SIZE = 4


# ==========================================
# GRAPH WEIGHTS
# ==========================================

GRAPH_SHARED_PAYMENT_SCORE = 35

GRAPH_SHARED_DEVICE_SCORE = 25

GRAPH_SHARED_PHONE_SCORE = 20

GRAPH_SHARED_BROWSER_SCORE = 18

GRAPH_SHARED_EMAIL_SCORE = 15

GRAPH_SHARED_ADDRESS_SCORE = 12

GRAPH_SHARED_IP_SCORE = 10

GRAPH_COMMUNITY_SCORE = 40


# ==========================================
# VELOCITY POLICY
# ==========================================

VELOCITY_CLUSTER_SCORE = 15


# ==========================================
# ACCOUNT TAKEOVER
# ==========================================

ATO_HIGH_SCORE = 35

ATO_MEDIUM_SCORE = 15


# ==========================================
# TRUST ENGINE
# ==========================================

INITIAL_TRUST_SCORE = 50

LOW_TRUST_THRESHOLD = 35

CRITICAL_TRUST_THRESHOLD = 20

TRUST_REWARD = 2

TRUST_PENALTY = 5


# ==========================================
# REPUTATION
# ==========================================

DEFAULT_REPUTATION = 50

MAX_REPUTATION = 100

MIN_REPUTATION = 0


# ==========================================
# ASN LEARNING
# ==========================================

ASN_MIN_TRANSACTIONS = 3

ASN_HIGH_FRAUD_RATIO = 0.40

ASN_HIGH_GRAPH_RATIO = 0.30

ASN_HIGH_GEO_RATIO = 0.40

ASN_HIGH_ATO_RATIO = 0.30


# ==========================================
# THREAT INTELLIGENCE
# ==========================================

THREAT_BLOCK_THRESHOLD = 3

THREAT_DECAY_RATE = 0.98


# ==========================================
# GEO INTELLIGENCE
# ==========================================

GEO_ANOMALY_SCORE = 15

IMPOSSIBLE_TRAVEL_SCORE = 25


# ==========================================
# RISK ENGINE
# ==========================================

LOW_RISK_MAX = 39

MEDIUM_RISK_MAX = 74

HIGH_RISK_MIN = 75

MAX_RISK_SCORE = 100

MIN_RISK_SCORE = 0