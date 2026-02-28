from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from src.database import get_db
from src.models.inventory import Inventory
from src.schemas.product_schema import InventoryResponse
from src.dependencies import get_current_admin
from src.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/inventory", tags=["Inventory"])


class InventoryUpdate(BaseModel):
    quantity: int
    reorder_level: int = 10


@router.get("/", response_model=List[InventoryResponse])
def list_inventory(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return (
        db.query(Inventory)
        .options(joinedload(Inventory.product))
        .all()
    )


@router.get("/{product_id}", response_model=InventoryResponse)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    inv = (
        db.query(Inventory)
        .options(joinedload(Inventory.product))
        .filter(Inventory.product_id == product_id)
        .first()
    )
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return inv


@router.put("/{product_id}", response_model=InventoryResponse)
def update_inventory(
    product_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    inv.quantity = payload.quantity
    inv.reorder_level = payload.reorder_level
    db.commit()
    db.refresh(inv)
    return inv
