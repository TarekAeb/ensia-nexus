from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    group_members,
    project_applications,
    project_participants,
    project_resources,
    projects,
    research_groups,
    research_labs,
    students,
    task_updates,
    tasks,
    teachers,
    users,
    auth,
)

from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = settings.API_V1_STR

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(students.router, prefix=API_PREFIX)
app.include_router(teachers.router, prefix=API_PREFIX)
app.include_router(research_labs.router, prefix=API_PREFIX)
app.include_router(research_groups.router, prefix=API_PREFIX)
app.include_router(group_members.router, prefix=API_PREFIX)
app.include_router(projects.router, prefix=API_PREFIX)
app.include_router(project_participants.router, prefix=API_PREFIX)
app.include_router(project_applications.router, prefix=API_PREFIX)
app.include_router(tasks.router, prefix=API_PREFIX)
app.include_router(task_updates.router, prefix=API_PREFIX)
app.include_router(project_resources.router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
