from fastapi import FastAPI
from pydantic import BaseModel
from engine.processor import process_transaction
from services.investigation_services import get_decision_by_id
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

@app.get("/decision/{decision_id}")
def fetch_decision(decision_id: str):
    record = get_decision_by_id(decision_id)

    if not record:
        raise HTTPException(status_code=404, detail="Decision not found")

    return record


@app.post("/analyze-transaction")
def analyze_transaction(event: TransactionEvent):
    result = process_transaction(event.dict())
    return result
