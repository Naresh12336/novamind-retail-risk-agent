from fastapi import FastAPI
from pydantic import BaseModel
from engine.processor import process_transaction

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


@app.post("/analyze-transaction")
def analyze_transaction(event: TransactionEvent):
    result = process_transaction(event.dict())
    return result
