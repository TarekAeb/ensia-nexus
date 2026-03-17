from app.domains.users.service import UserService
from app.domains.users.schemas import UserUpdate


def get_my_profile():
    return UserService.get_user_profile()


def update_my_profile(profile_data: UserUpdate):
    return UserService.update_user_profile(profile_data)


def get_user(user_id: int):
    return UserService.get_user_by_id(user_id)


def list_users():
    return UserService.list_users()


def delete_user(user_id: int):
    return UserService.delete_user(user_id)
