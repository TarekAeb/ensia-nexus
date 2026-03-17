from app.domains.projects.service import ProjectService
from app.domains.projects.schemas import ProjectCreate, ProjectUpdate, ParticipantCreate


def list_projects():
    return ProjectService.list_projects()


def get_project(project_id: int):
    return ProjectService.get_project(project_id)


def create_project(project_data: ProjectCreate):
    return ProjectService.create_project(project_data)


def update_project(project_id: int, project_data: ProjectUpdate):
    return ProjectService.update_project(project_id, project_data)


def delete_project(project_id: int):
    return ProjectService.delete_project(project_id)


def list_participants(project_id: int):
    return ProjectService.list_participants(project_id)


def add_participant(project_id: int, participant_data: ParticipantCreate):
    return ProjectService.add_participant(project_id, participant_data)


def remove_participant(project_id: int, user_id: int):
    return ProjectService.remove_participant(project_id, user_id)
