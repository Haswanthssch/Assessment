from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime
from src.services.log_service import get_activity_logs, get_order_history
from src.dependencies import get_current_admin
from src.models.user import User

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/activity")
def activity_logs(
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    limit: int = Query(100, le=500),
    _: User = Depends(get_current_admin),
):
    logs = get_activity_logs(date_from=date_from, date_to=date_to, limit=limit)
    return {"count": len(logs), "logs": logs}


@router.get("/order-history")
def order_history_logs(
    order_id: Optional[int] = Query(None),
    limit: int = Query(50, le=200),
    _: User = Depends(get_current_admin),
):
    history = get_order_history(order_id=order_id, limit=limit)
    return {"count": len(history), "history": history}
