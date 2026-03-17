from fastapi import APIRouter

from app.domains.users import users_router
from app.domains.auth import auth_router
from app.domains.labs import labs_router
from app.domains.groups import groups_router
from app.domains.projects import projects_router
from app.domains.applications import applications_router
from app.domains.tasks import tasks_router
from app.domains.resources import resources_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(labs_router)
api_router.include_router(groups_router)
api_router.include_router(projects_router)
api_router.include_router(applications_router)
api_router.include_router(tasks_router)
api_router.include_router(resources_router)