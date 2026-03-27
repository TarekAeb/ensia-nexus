from sqlalchemy import BigInteger, CheckConstraint, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "role IN ('STUDENT','TEACHER','ADMIN', 'PARTNER')",
            name="users_role_check",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    institution: Mapped[str | None] = mapped_column(Text, nullable=True)
    department: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    website: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    student: Mapped["Student"] = relationship(
        "Student", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    teacher: Mapped["Teacher"] = relationship(
        "Teacher", back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    group_memberships: Mapped[list["GroupMember"]] = relationship(
        "GroupMember", back_populates="user", cascade="all, delete-orphan"
    )
    project_participations: Mapped[list["ProjectParticipant"]] = relationship(
        "ProjectParticipant", back_populates="user", cascade="all, delete-orphan"
    )
    created_projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="creator", foreign_keys="Project.created_by"
    )
    validated_groups: Mapped[list["ResearchGroup"]] = relationship(
        "ResearchGroup",
        back_populates="validator",
        foreign_keys="ResearchGroup.validated_by_admin_id",
    )
    task_updates: Mapped[list["TaskUpdate"]] = relationship(
        "TaskUpdate", back_populates="author", foreign_keys="TaskUpdate.author_user_id"
    )
    reviewed_applications: Mapped[list["ProjectApplication"]] = relationship(
        "ProjectApplication",
        back_populates="reviewer",
        foreign_keys="ProjectApplication.reviewed_by",
    )
    created_tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="creator", foreign_keys="Task.created_by"
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="assignee", foreign_keys="Task.assignee_user_id"
    )
    created_resources: Mapped[list["ProjectResource"]] = relationship(
        "ProjectResource", back_populates="creator"
    )
    student_cvs: Mapped[list["StudentCV"]] = relationship(
        "StudentCV", back_populates="student", cascade="all, delete-orphan"
    )

    @property
    def is_teacher(self) -> bool:
        return self.role == "TEACHER"

    @property
    def is_admin(self) -> bool:
        return self.role == "ADMIN"

    @property
    def is_student(self) -> bool:
        return self.role == "STUDENT"

