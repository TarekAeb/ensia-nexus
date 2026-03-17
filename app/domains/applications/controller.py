from app.domains.applications.service import ApplicationService


def apply_to_project():
    return ApplicationService.apply_for_project()


def list_my_applications():
    return ApplicationService.list_my_applications()


def list_project_applications(project_id: int):
    return ApplicationService.list_project_applications(project_id)


def accept_application(application_id: int):
    return ApplicationService.accept_application(application_id)


def reject_application(application_id: int):
    return ApplicationService.reject_application(application_id)
