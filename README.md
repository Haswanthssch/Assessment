# InventoryOS — Cloud-Native Inventory & Order Management System

A full-stack, containerized inventory and order management system with:
- **Admin Dashboard** (Bootstrap 5)
- **User Storefront** (Browse, Cart, Checkout)
- **FastAPI** REST API
- **Flask** HTML template serving
- **PostgreSQL** (Docker) via **SQLAlchemy ORM**
- **MongoDB Atlas** for Activity Logs
- **Docker** containerization
- **GitHub Actions** CI/CD

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
cd docker
docker-compose up --build
```

Starts:
- Backend (Flask + FastAPI) on **http://localhost:5000**
- PostgreSQL on port 5432

### Option 2: Local Dev

```bash
# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env
# Edit .env with your settings

# Seed database
python db/init_db.py

# Run server
uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload
```

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `http://localhost:5000/admin/login` | Admin dashboard login |
| `http://localhost:5000/login` | User storefront login |
| `http://localhost:5000/health` | Health check |
| `http://localhost:5000/api/docs` | Interactive API docs (Swagger) |
| `http://localhost:5000/api/redoc` | ReDoc API docs |

### Default Admin Credentials
- **Email:** `admin@admin.com`
- **Password:** `admin123`

---

## 📁 Project Structure

```
Assessment/
├── src/
│   ├── main.py          # FastAPI app entry point (mounts Flask)
│   ├── web_app.py       # Flask app (HTML template routes)
│   ├── config.py        # Config from env vars
│   ├── database.py      # PostgreSQL + MongoDB connections
│   ├── dependencies.py  # JWT auth dependency injection
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic request/response models
│   ├── routes/          # FastAPI REST API routers
│   └── services/        # Auth + MongoDB log services
├── db/
│   ├── schema.sql       # PostgreSQL DDL schema
│   ├── seed.sql         # Sample data
│   └── init_db.py       # Python DB seeder
├── templates/           # Jinja2 HTML templates (Bootstrap 5)
│   ├── admin/           # Admin dashboard pages
│   └── user/            # User storefront pages
├── static/              # CSS & JS assets
├── docker/              # Dockerfile
├── tests/               # Pytest tests
├── .github/workflows/   # GitHub Actions CI/CD
├── docker-compose.yml
└── requirements.txt
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | None | Register user |
| POST | `/api/v1/auth/login` | None | Login → JWT |
| GET | `/api/v1/products/` | None | List products |
| POST | `/api/v1/products/` | Admin | Create product |
| PUT | `/api/v1/products/{id}` | Admin | Update product |
| DELETE | `/api/v1/products/{id}` | Admin | Soft delete |
| GET | `/api/v1/orders/` | User/Admin | List orders |
| POST | `/api/v1/orders/` | User | Place order |
| PUT | `/api/v1/orders/{id}/status` | Admin | Update status |
| GET | `/api/v1/inventory/` | Admin | View stock |
| PUT | `/api/v1/inventory/{pid}` | Admin | Update stock |
| GET | `/api/v1/admin/stats` | Admin | Dashboard stats |
| GET | `/api/v1/logs/activity` | Admin | MongoDB logs |
| GET | `/api/v1/logs/order-history` | Admin | Order history |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🐳 CI/CD

GitHub Actions pipeline (`.github/workflows/ci.yml`):
1. **Lint** – flake8
2. **Test** – pytest with PostgreSQL service container
3. **Docker Build & Push** – on `main` branch push

**Required GitHub Secrets:**
- `MONGODB_URI` – your MongoDB Atlas URI
- `DOCKER_USERNAME` – Docker Hub username
- `DOCKER_TOKEN` – Docker Hub token
