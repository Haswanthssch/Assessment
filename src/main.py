import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware

from src.routes import auth, users, products, orders, inventory, admin, logs
from src.database import engine, Base
from src.models import User, Product, Order, OrderItem, Inventory  # noqa – registers models
from src.web_app import flask_app

# ─── Create all tables on startup (fault-tolerant) ───────────────────────────
import logging
_log = logging.getLogger("inventory")
try:
    Base.metadata.create_all(bind=engine)
    _log.info("✅  Database tables created / verified.")
except Exception as _db_err:
    _log.warning(
        f"⚠️  Could not connect to the database at startup: {_db_err}\n"
        "    Make sure the database is running (see README). App will retry on first request."
    )

# ─── FastAPI REST API ──────────────────────────────────────────────────────
api = FastAPI(
    title="Inventory & Order Management – REST API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers under /api/v1
for router in [auth.router, users.router, products.router,
               orders.router, inventory.router, admin.router, logs.router]:
    api.include_router(router, prefix="/api/v1")


@api.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Inventory Management API"}


# ─── Mount Flask (HTML/Web UI) at root ───────────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
api.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
api.mount("/", WSGIMiddleware(flask_app))

app = api
