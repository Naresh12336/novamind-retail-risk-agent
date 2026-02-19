from fastapi import FastAPI
from pydantic import BaseModel
from engine.processor import process_transaction
from services.investigation_services import get_decision_by_id, get_customer_history, get_recent_customer_events
from fastapi import HTTPException



app = FastAPI(title="NovaMind Risk Service")


class TransactionEvent(BaseModel):
    transaction_id: str
    customer_id: str
    transaction_type: str
    description: str
    amount: float
    account_age_days: int
    refund_count_last_30_days: int
    timestamp: str

def emit_alert(result: dict):
    customer_id = result.get("customer_id")

    recent_events = get_recent_customer_events(customer_id)

    alert_payload = {
        "decision_id": result.get("decision_id"),
        "transaction_id": result.get("transaction_id"),
        "customer_id": customer_id,
        "risk_category": result.get("risk_category"),
        "confidence_level": result.get("confidence_level"),
        "recommended_action": result.get("recommended_action"),
        "recent_activity": recent_events
    }

    print("\n=== ALERT TRIGGERED ===")
    print(alert_payload)

@app.get("/decision/{decision_id}")
def fetch_decision(decision_id: str):
    record = get_decision_by_id(decision_id)

    if not record:
        raise HTTPException(status_code=404, detail="Decision not found")

    return record

@app.get("/customer-history/{customer_id}")
def fetch_customer_history(customer_id: str):
    history = get_customer_history(customer_id)

    if not history:
        raise HTTPException(status_code=404, detail="No records found")

    return {
        "customer_id": customer_id,
        "events": history
    }

@app.post("/analyze-transaction")
def analyze_transaction(event: TransactionEvent):
    result = process_transaction(event.dict())
    return result
