from collections import defaultdict

ip_reputation = defaultdict(lambda: {
    "total_transactions": 0,
    "high_risk_transactions": 0,
    "blocked_transactions": 0,
    "linked_customers": set()
})

email_reputation = defaultdict(lambda: {
    "total_transactions": 0,
    "high_risk_transactions": 0,
    "blocked_transactions": 0,
    "linked_customers": set()
})

device_reputation = defaultdict(lambda: {
    "total_transactions": 0,
    "high_risk_transactions": 0,
    "blocked_transactions": 0,
    "linked_customers": set()
})