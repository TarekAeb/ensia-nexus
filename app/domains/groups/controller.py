from app.domains.groups.service import GroupService
from app.domains.groups.schemas import GroupCreate, GroupUpdate


def list_groups():
    return GroupService.list_groups()


def get_group(group_id: int):
    return GroupService.get_group(group_id)


def create_group(group_data: GroupCreate):
    return GroupService.create_group(group_data)


def update_group(group_id: int, group_data: GroupUpdate):
    return GroupService.update_group(group_id, group_data)
