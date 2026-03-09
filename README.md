# Research Lab API

A complete, production-ready FastAPI application for managing Research Labs, Groups, Projects, Tasks, and Members.

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLAlchemy (async) | ORM with async support |
| asyncpg | Async PostgreSQL driver |
| Alembic | Database migrations |
| Pydantic v2 | Data validation & serialization |
| PostgreSQL | Primary database |

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ensia-nexus
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/fastapi_research_lab
SECRET_KEY=your-secret-key-here
```

## Database Migration

Run Alembic migrations to create all tables:

```bash
alembic upgrade head
```

To auto-generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "description of changes"
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── main.py                    # FastAPI application entry point
├── database.py                # Async SQLAlchemy engine and session
├── config.py                  # Pydantic settings
├── models/                    # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── teacher.py
│   ├── research_lab.py
│   ├── research_group.py
│   ├── group_member.py
│   ├── project.py
│   ├── project_participant.py
│   ├── project_application.py
│   ├── task.py
│   ├── task_update.py
│   └── project_resource.py
├── schemas/                   # Pydantic v2 schemas
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── teacher.py
│   ├── research_lab.py
│   ├── research_group.py
│   ├── group_member.py
│   ├── project.py
│   ├── project_participant.py
│   ├── project_application.py
│   ├── task.py
│   ├── task_update.py
│   └── project_resource.py
├── crud/                      # Async CRUD operations
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── teacher.py
│   ├── research_lab.py
│   ├── research_group.py
│   ├── group_member.py
│   ├── project.py
│   ├── project_participant.py
│   ├── project_application.py
│   ├── task.py
│   ├── task_update.py
│   └── project_resource.py
├── routers/                   # FastAPI routers
│   ├── __init__.py
│   ├── users.py
│   ├── students.py
│   ├── teachers.py
│   ├── research_labs.py
│   ├── research_groups.py
│   ├── group_members.py
│   ├── projects.py
│   ├── project_participants.py
│   ├── project_applications.py
│   ├── tasks.py
│   ├── task_updates.py
│   └── project_resources.py
alembic/                       # Database migrations
│   env.py
│   script.py.mako
│   versions/
alembic.ini
requirements.txt
.env.example
```

## API Endpoints

| Prefix | Resource |
|---|---|
| `/api/v1/users` | User management |
| `/api/v1/students` | Student profiles |
| `/api/v1/teachers` | Teacher profiles |
| `/api/v1/labs` | Research labs |
| `/api/v1/groups` | Research groups |
| `/api/v1/group-members` | Group membership |
| `/api/v1/projects` | Projects |
| `/api/v1/project-participants` | Project participants |
| `/api/v1/project-applications` | Project applications |
| `/api/v1/tasks` | Tasks |
| `/api/v1/task-updates` | Task updates/logs |
| `/api/v1/project-resources` | Project resources |

Each endpoint group supports:
- `GET /` — list with pagination (`skip`, `limit`)
- `GET /{id}` — get by ID (404 if not found)
- `POST /` — create (returns 201)
- `PUT /{id}` — partial update (404 if not found)
- `DELETE /{id}` — delete (204 on success, 404 if not found)

## Health Check

- `GET /` → `{"status": "ok", "version": "1.0.0"}`
- `GET /health` → `{"status": "healthy"}`

## Future Enhancements

- **Authentication & JWT**: Implement token-based authentication using OAuth2 with JWT tokens
- **Role-Based Access Control (RBAC)**: Restrict endpoints based on user roles (STUDENT, MCA, PROFESSOR, DOCTOR, ADMIN)
- **Rate Limiting**: Protect the API from abuse
- **Caching**: Add Redis-based caching for frequently accessed data
- **File Uploads**: Support for document and dataset file uploads
