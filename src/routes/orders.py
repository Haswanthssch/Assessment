from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from src.database import get_db
from src.models.order import Order
from src.models.order_item import OrderItem
from src.models.inventory import Inventory
from src.schemas.order_schema import OrderCreate, OrderResponse, OrderStatusUpdate
from src.dependencies import get_current_user, get_current_admin
from src.models.user import User
from src.services.log_service import log_order_status, log_user_activity

router = APIRouter(prefix="/orders", tags=["Orders"])


def _serialize_order(order: Order) -> dict:
    items = []
    for i in order.items:
        items.append({
            "id": i.id,
            "product_id": i.product_id,
            "quantity": i.quantity,
            "unit_price": i.unit_price,
            "subtotal": i.quantity * i.unit_price,
            "product_name": i.product.name if i.product else "Deleted",
        })
    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address,
        "created_at": order.created_at,
        "items": items,
        "username": order.user.username if order.user else None,
    }


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product), joinedload(Order.user))
    )
    if current_user.role != "admin":
        q = q.filter(Order.user_id == current_user.id)
    orders = q.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return [_serialize_order(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product), joinedload(Order.user))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return _serialize_order(order)


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total = sum(i.quantity * i.unit_price for i in payload.items)
    order = Order(user_id=current_user.id, total_amount=total,
                  shipping_address=payload.shipping_address, status="pending")
    db.add(order)
    db.flush()

    for item_data in payload.items:
        # Reduce inventory
        inv = db.query(Inventory).filter(Inventory.product_id == item_data.product_id).first()
        if inv:
            if inv.quantity < item_data.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item_data.product_id}")
            inv.quantity -= item_data.quantity

        item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
        )
        db.add(item)

    db.commit()
    db.refresh(order)
    log_user_activity(current_user.id, current_user.username, "create_order", {"order_id": order.id, "total": total})
    log_order_status(order.id, current_user.id, "none", "pending")

    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product), joinedload(Order.user))
        .filter(Order.id == order.id)
        .first()
    )
    return _serialize_order(order)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    old_status = order.status
    order.status = payload.status
    db.commit()
    log_order_status(order_id, order.user_id, old_status, payload.status)
    db.refresh(order)
    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product), joinedload(Order.user))
        .filter(Order.id == order_id)
        .first()
    )
    return _serialize_order(order)
