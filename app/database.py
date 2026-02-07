from pydantic import BaseModel
from typing import List, Dict, Optional

# 1. Define our Data Models
class P2POrder(BaseModel):
    order_id: str
    amount: float
    currency: str
    status: str  # 'pending', 'verified', 'flagged'
    buyer_name: str
    seller_name: str
    risk_score: int = 0
    verification_notes: Optional[str] = None

# 2. Mock Data for Database
MOCK_ORDERS: Dict[str, P2POrder] = {
    "ORD-101": P2POrder(
        order_id="ORD-101", 
        amount=15500, 
        currency="NGN", 
        status="pending", 
        buyer_name="Adepitan Rashid Adetunji", 
        seller_name="Deriv_Merchant_01"
    ),
    "ORD-102": P2POrder(
        order_id="ORD-102", 
        amount=1500.0, 
        currency="USD", 
        status="pending", 
        buyer_name="Crypto_King", 
        seller_name="Deriv_Merchant_02"
    )
}

# 3. Helper functions to simulate DB queries
def get_order_by_id(order_id: str) -> Optional[P2POrder]:
    return MOCK_ORDERS.get(order_id)

def update_order_status(order_id: str, status: str, risk_score: int, notes: str):
    if order_id in MOCK_ORDERS:
        MOCK_ORDERS[order_id].status = status
        MOCK_ORDERS[order_id].risk_score = risk_score
        MOCK_ORDERS[order_id].verification_notes = notes