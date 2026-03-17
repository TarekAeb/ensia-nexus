from app.domains.labs.service import LabService
from app.domains.labs.schemas import LabCreate, LabUpdate


def list_labs():
    return LabService.list_labs()


def get_lab(lab_id: int):
    return LabService.get_lab(lab_id)


def create_lab(lab_data: LabCreate):
    return LabService.create_lab(lab_data)


def update_lab(lab_id: int, lab_data: LabUpdate):
    return LabService.update_lab(lab_id, lab_data)


def delete_lab(lab_id: int):
    return LabService.delete_lab(lab_id)
