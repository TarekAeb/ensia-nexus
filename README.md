# Research Collaboration Platform API

A complete, production-ready FastAPI application for managing Research Labs, Groups, Projects, Tasks, and Members. This platform facilitates collaboration between students and teachers in a research environment.

Built with **FastAPI**, **PostgreSQL**, and a **modular architecture**.

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLAlchemy (async) | ORM with async support |
| asyncpg | Async PostgreSQL driver |
| Alembic | Database migrations |
| Pydantic v2 | Data validation & serialization |
| PostgreSQL | Primary database |
| JWT (python-jose) | Authentication & Security |
| Pytest | Testing framework |
| Uvicorn | ASGI server |

---

## 📁 Project Structure

The project follows a hybrid architecture, transitioning towards a domain-driven design:

```
app/
├── main.py                    # FastAPI application entry point
├── core/                      # Core configurations
│   ├── config.py              # Pydantic settings
│   ├── database.py            # Async SQLAlchemy engine
│   ├── auth.py                # JWT & Authentication logic
│   ├── security.py            # Security utilities
│   └── permissions.py         # Role-based access control
├── api/                       # Unified API routing
│   └── router.py
├── domains/                   # Domain-specific logic (New Modular approach)
│   ├── auth/                  # Auth services, routes, schemas
│   ├── users/                 # User domain
│   ├── labs/                  # Research Labs domain
│   └── ...                    # (Groups, Projects, Applications, Tasks, Resources)
├── infrastructure/            # Data access & external services
│   ├── database/models/       # SQLAlchemy ORM models
│   └── repositories/          # Data repository patterns
├── models/                    # Legacy SQLAlchemy models (Flat structure)
├── schemas/                   # Legacy Pydantic schemas (Flat structure)
├── routers/                   # Legacy API routers (Flat structure)
└── tests/                     # Automated tests
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd backend
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Copy the example environment file and fill in your values:
```bash
cp .env.example .env
```

Edit `.env` (ensure PostgreSQL is running):
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/research_platform
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Database Migration
Run Alembic migrations to create all tables:
```bash
alembic upgrade head
```

---

## 🏃 Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📌 Main Features

- **User Authentication & RBAC**: JWT-based auth with roles (STUDENT, TEACHER, ADMIN).
- **Research Management**: Manage labs, groups, and memberships.
- **Projects & Collaboration**: Create projects, track participation, and manage applications.
- **Task Tracking**: Task creation, updates, and progress logs.
- **Resource Sharing**: Share papers, datasets, and repositories.
- **Permissions System**: Fine-grained access control using FastAPI dependencies.

---

## 🧪 Testing

Run the test suite using pytest:
```bash
pytest
```

---

## 🛡️ Health & Monitoring
- `GET /` → `{"status": "ok", "version": "1.0.0"}`
- `GET /health` → `{"status": "healthy"}`

---

## 🔮 Future Enhancements
- **Rate Limiting**: Protect the API from abuse.
- **Caching**: Add Redis-based caching for frequently accessed data.
- **File Uploads**: Support for document and dataset file uploads.
- **Real-time Notifications**: WebSocket-based updates for tasks and applications.

---

## 📄 Notes & License
- `.env` is ignored in git; do not commit secrets.
- This project is for educational purposes.
": "1.0.0"}`
- `GET /health` → `{"status": "healthy"}`

## Future Enhancements

- **Authentication & JWT**: Implement token-based authentication using OAuth2 with JWT tokens
- **Role-Based Access Control (RBAC)**: Restrict endpoints based on user roles (STUDENT, MCA, PROFESSOR, DOCTOR, ADMIN)
- **Rate Limiting**: Protect the API from abuse
- **Caching**: Add Redis-based caching for frequently accessed data
- **File Uploads**: Support for document and dataset file uploads
