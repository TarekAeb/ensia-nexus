from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user

from app.infrastructure.repositories.group_repository import GroupRepository
from app.infrastructure.repositories.project_repository import ProjectRepository
from app.infrastructure.repositories.teacher_repository import TeacherRepository


# todo: add more checks (e.g. in project role, resource ownership, etc.)
def permission_guard(
        roles: list[str] | None = None,
        teacher_grades: list[str] | None = None,
        group_member: bool = False,
        project_member: bool = False
):
    def guard(
            group_id: int | None = None,
            project_id: int | None = None,
            user=Depends(get_current_user),
    ):

        # -------------------------------------
        # ROLE CHECK
        # -------------------------------------

        if roles and user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Role not allowed"
            )

        # -------------------------------------
        # TEACHER GRADE CHECK
        # -------------------------------------

        if teacher_grades:

            teacher = TeacherRepository.get_teacher(
                user.id
            )

            if not teacher or teacher.grade not in teacher_grades:
                raise HTTPException(
                    status_code=403,
                    detail="Teacher grade not allowed"
                )

        # -------------------------------------
        # GROUP MEMBERSHIP CHECK
        # -------------------------------------

        if group_member:

            member = GroupRepository.is_member(
                group_id,
                user.id
            )

            if not member:
                raise HTTPException(
                    status_code=403,
                    detail="Not member of group"
                )

        # -------------------------------------
        # PROJECT MEMBERSHIP CHECK
        # -------------------------------------

        if project_member:

            member = ProjectRepository.is_project_member(
                project_id,
                user.id
            )

            if not member:
                raise HTTPException(
                    status_code=403,
                    detail="Not member of project"
                )

        return user

    return guard
