from app.domains.resources.service import ResourceService
from app.domains.resources.schemas import ResourceCreate


def list_resources(project_id: int):
    return ResourceService.list_resources(project_id)


def add_resource(resource_data: ResourceCreate):
    return ResourceService.add_resource(resource_data)


def delete_resource(resource_id: int):
    return ResourceService.delete_resource(resource_id)
