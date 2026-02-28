from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"),
                        unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, default=10)
    last_updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    product = relationship("Product", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory product_id={self.product_id} qty={self.quantity}>"
