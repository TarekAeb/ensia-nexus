from fastapi import APIRouter
from typing import List
from app.domains.applications.schemas import ApplicationCreate, ApplicationResponse
from app.domains.applications import controller as application_controller

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


# Spec: POST /projects/{project_id}/apply
@router.post("/apply", response_model=ApplicationResponse)
def apply_for_project(application_data: ApplicationCreate):
    return application_controller.apply_to_project()


@router.get("/me", response_model=List[ApplicationResponse])
def list_my_applications():
    return application_controller.list_my_applications()


# Spec: GET /projects/{project_id}/applications
# This might conflict with the prefix if not careful, assuming this router is /applications
# But if it's unrelated to prefix, or we need to query by project_id in query param
@router.get("/", response_model=List[ApplicationResponse])
def list_project_applications(project_id: int):
    return application_controller.list_project_applications(project_id)


@router.patch("/{application_id}/accept", response_model=ApplicationResponse)
def accept_application(application_id: int):
    return application_controller.accept_application(application_id)


@router.patch("/{application_id}/reject", response_model=ApplicationResponse)
def reject_application(application_id: int):
    return application_controller.reject_application(application_id)
