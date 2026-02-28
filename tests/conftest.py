"""
Pytest configuration and shared fixtures.
Uses an isolated SQLite in-memory DB for SQL tests and mocks MongoDB.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ─── Use SQLite for tests (no PostgreSQL needed locally) ────────────────────
TEST_DB_URL = "sqlite:///./test.db"

# Patch env before any app imports
import os  # noqa: E402
os.environ["DATABASE_URL"] = TEST_DB_URL
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["FLASK_SECRET_KEY"] = "test-flask-secret"
os.environ["MONGODB_URI"] = "mongodb://localhost:27017"
os.environ["MONGODB_DB"] = "test_logs"

from src.database import Base, get_db  # noqa: E402
from src.main import api  # FastAPI app  # noqa: E402


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    TestSession = sessionmaker(bind=db_engine)
    session = TestSession()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    api.dependency_overrides[get_db] = override_get_db
    with TestClient(api) as c:
        yield c
    api.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_token(client):
    """Register an admin user and return JWT token."""
    res = client.post("/api/v1/auth/register", json={
        "username": "testadmin",
        "email": "testadmin@test.com",
        "password": "admin123",
        "role": "admin"
    })
    if res.status_code not in (200, 201, 400):
        raise RuntimeError(f"Admin register failed: {res.text}")
    login = client.post("/api/v1/auth/login", json={
        "email": "testadmin@test.com",
        "password": "admin123"
    })
    return login.json()["access_token"]


@pytest.fixture(scope="function")
def user_token(client):
    """Register a regular user and return JWT token."""
    client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "testuser@test.com",
        "password": "user123",
        "role": "user"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "testuser@test.com",
        "password": "user123"
    })
    return login.json()["access_token"]
