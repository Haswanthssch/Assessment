"""
Database initialisation helper.
Run: python db/init_db.py
Creates all tables and loads seed data.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.database import engine, Base, SessionLocal
from src.models import User, Product, Order, OrderItem, Inventory  # noqa
from src.services.auth_service import hash_password

def init():
    print("⏳  Creating tables…")
    Base.metadata.create_all(bind=engine)
    print("✅  Tables created.")

    db = SessionLocal()
    try:
        # Admin user
        if not db.query(User).filter(User.email == "admin@admin.com").first():
            admin = User(
                username="admin",
                email="admin@admin.com",
                password_hash=hash_password("admin123"),
                role="admin",
            )
            db.add(admin)
            print("✅  Admin user created  (admin@admin.com / admin123)")

        # Sample products
        sample_products = [
            dict(name="Laptop Pro 15", description="High-performance laptop 16GB RAM",
                 price=999.99, category="Electronics",
                 image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"),
            dict(name="Wireless Mouse", description="Ergonomic 2.4GHz wireless mouse",
                 price=29.99, category="Electronics",
                 image_url="https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400"),
            dict(name="Mechanical Keyboard", description="RGB backlit keyboard 104 keys",
                 price=89.99, category="Electronics",
                 image_url="https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400"),
            dict(name="Office Chair", description="Ergonomic chair with lumbar support",
                 price=349.99, category="Furniture",
                 image_url="https://images.unsplash.com/photo-1589384267710-7a170981ca78?w=400"),
            dict(name="Standing Desk", description="Height-adjustable standing desk 140x70cm",
                 price=499.99, category="Furniture",
                 image_url="https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400"),
            dict(name="USB-C Hub", description="7-in-1 USB-C hub with 4K HDMI",
                 price=49.99, category="Electronics",
                 image_url="https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=400"),
            dict(name='Monitor 27"', description="4K IPS 27-inch display with HDR",
                 price=449.99, category="Electronics",
                 image_url="https://images.unsplash.com/photo-1547082299-de196ea013d6?w=400"),
            dict(name="Notebook A5", description="Premium hard-cover ruled notebook",
                 price=12.99, category="Stationery",
                 image_url="https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400"),
            dict(name="Pen Set", description="12 premium ballpoint pens",
                 price=8.99, category="Stationery",
                 image_url="https://images.unsplash.com/photo-1583485088034-697b5bc36b08?w=400"),
            dict(name="Desk Lamp", description="LED lamp with adjustable brightness",
                 price=39.99, category="Furniture",
                 image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400"),
        ]

        for p_data in sample_products:
            if not db.query(Product).filter(Product.name == p_data["name"]).first():
                product = Product(**p_data)
                db.add(product)
                db.flush()
                inv = Inventory(product_id=product.id, quantity=50, reorder_level=10)
                db.add(inv)

        db.commit()
        print("✅  Sample products + inventory seeded.")
    finally:
        db.close()

    print("\n🚀  Database ready! Visit http://localhost:5000/admin/login")
    print("    Admin credentials: admin@admin.com / admin123")


if __name__ == "__main__":
    init()
