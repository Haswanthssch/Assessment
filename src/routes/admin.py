from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.database import get_db
from src.models.user import User
from src.models.product import Product
from src.models.order import Order
from src.models.inventory import Inventory
from src.dependencies import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    total_users = db.query(func.count(User.id)).filter(User.role == "user").scalar()
    total_products = db.query(func.count(Product.id)).filter(Product.is_active).scalar()
    total_orders = db.query(func.count(Order.id)).scalar()
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status.in_(["confirmed", "shipped", "delivered"])
    ).scalar() or 0.0

    orders_by_status = (
        db.query(Order.status, func.count(Order.id))
        .group_by(Order.status)
        .all()
    )

    low_stock = (
        db.query(Inventory)
        .filter(Inventory.quantity <= Inventory.reorder_level)
        .count()
    )

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "orders_by_status": {s: c for s, c in orders_by_status},
        "low_stock_alerts": low_stock,
    }
