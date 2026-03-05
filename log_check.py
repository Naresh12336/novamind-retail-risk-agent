import json

count = 0
with open("logs/decision_history.jsonl") as f:
    for line in f:
        r = json.loads(line)
        if r.get("primary_factor") == "repeat_refund_behavior" and r.get("refund_count_last_30_days") == 7:
            count += 1

print("Matching records:", count)