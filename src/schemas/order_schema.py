from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class OrderCreate(BaseModel):
    shipping_address: Optional[str] = None
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: str  # pending | confirmed | shipped | delivered | cancelled


class OrderItemResponse(BaseModel):
    id: int
    product_id: Optional[int]
    quantity: int
    unit_price: float
    subtotal: float
    product_name: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    shipping_address: Optional[str]
    created_at: Optional[datetime]
    items: List[OrderItemResponse] = []
    username: Optional[str] = None

    model_config = {"from_attributes": True}
