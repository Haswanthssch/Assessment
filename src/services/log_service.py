from datetime import datetime, timezone
from typing import Optional, List
from src.database import activity_logs_col, order_history_col


def log_user_activity(user_id: int, username: str, action: str, details: dict = None):
    """Insert an activity log entry into MongoDB."""
    doc = {
        "user_id": user_id,
        "username": username,
        "action": action,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc),
    }
    activity_logs_col.insert_one(doc)


def log_order_status(order_id: int, user_id: int, old_status: str, new_status: str):
    """Insert an order status change into MongoDB."""
    doc = {
        "order_id": order_id,
        "user_id": user_id,
        "old_status": old_status,
        "new_status": new_status,
        "timestamp": datetime.now(timezone.utc),
    }
    order_history_col.insert_one(doc)


def get_activity_logs(
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: int = 100,
) -> List[dict]:
    """Fetch activity logs filtered by date range."""
    query = {}
    if date_from or date_to:
        query["timestamp"] = {}
        if date_from:
            query["timestamp"]["$gte"] = date_from
        if date_to:
            query["timestamp"]["$lte"] = date_to

    cursor = activity_logs_col.find(query).sort("timestamp", -1).limit(limit)
    logs = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        logs.append(doc)
    return logs


def get_order_history(order_id: Optional[int] = None, limit: int = 50) -> List[dict]:
    """Fetch order status history."""
    query = {}
    if order_id:
        query["order_id"] = order_id

    cursor = order_history_col.find(query).sort("timestamp", -1).limit(limit)
    docs = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        docs.append(doc)
    return docs
