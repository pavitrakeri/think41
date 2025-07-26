from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime

class ProductResponse(BaseModel):
    product_id: str
    product_name: str
    category: str
    price: float
    stock_quantity: int
    description: str

class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    order_date: datetime
    status: str
    total_amount: float

class OrderItemResponse(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    price: float

class ConversationResponse(BaseModel):
    id: int
    conversation_id: str
    user_message: str
    ai_response: str
    created_at: datetime 