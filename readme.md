# Research Collaboration Platform API

A backend system for managing research labs, groups, projects, and collaboration between students and teachers.

Built with **FastAPI**, **PostgreSQL**, and a **modular architecture**.

---

## 🚀 Tech Stack

* **FastAPI** – Backend framework
* **PostgreSQL** – Database
* **SQLAlchemy** – ORM / DB access
* **Pydantic** – Data validation
* **JWT (python-jose)** – Authentication
* **Uvicorn** – ASGI server

---

## 📁 Project Structure

```
app/
│
├── main.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── auth.py
│   ├── security.py
│   └── permissions.py
│
├── api/
│   └── router.py
│
├── domains/
│   ├── auth/
│   ├── users/
│   ├── labs/
│   ├── groups/
│   ├── projects/
│   ├── applications/
│   ├── tasks/
│   └── resources/
│
├── infrastructure/
│   ├── database/models/
│   └── repositories/
│
└── tests/
```

---

## ⚙️ Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd backend
```

---

### 2. Create virtual environment

```
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=research_platform

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 5. Create PostgreSQL database

```
CREATE DATABASE research_platform;
```

---

### 6. Run the server

```
uvicorn app.main:app --reload
```

---

## 📚 API Documentation

After running the server:

* Swagger UI:

```
http://127.0.0.1:8000/docs
```

* ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 🔐 Authentication

The API uses **JWT (Bearer Token)**.

Example header:

```
Authorization: Bearer <your_token>
```

---

## 📌 Main Features

* User authentication and roles (Student, Teacher, Admin)
* Research labs and groups management
* Project creation and participation
* Task management and progress tracking
* Application system for students
* Resource sharing (papers, datasets, repos)

---

## 🛡️ Permissions System

Custom permission system using FastAPI dependencies:

* Role-based access (ADMIN, TEACHER, STUDENT)
* Group membership validation
* Project membership validation

Example:

```
Depends(permission_guard(
    roles=["ADMIN"],
    project_member=True
))
```

---

## 🧪 Testing

Run tests:

```
pytest
```

---

## ⚠️ Notes

* `.env` is ignored in git (do not commit secrets)
* Database schema is created automatically (dev mode)
* Use migrations (Alembic) for production

---

## 📄 License

This project is for educational purposes.
