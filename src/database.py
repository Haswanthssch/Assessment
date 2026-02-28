from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pymongo import MongoClient
from src.config import get_settings

settings = get_settings()

# ─── PostgreSQL ───────────────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency – yields a SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── MongoDB ─────────────────────────────────────────────────────────────────
mongo_client = MongoClient(settings.MONGODB_URI)
mongo_db = mongo_client[settings.MONGODB_DB]
activity_logs_col = mongo_db["activity_logs"]
order_history_col = mongo_db["order_history"]
