from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint(
            "visibility IN ('PUBLIC','PRIVATE')",
            name="projects_visibility_check",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("research_groups.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    visibility: Mapped[str] = mapped_column(String(10), nullable=False, default="PRIVATE")
    created_by: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    group: Mapped["ResearchGroup"] = relationship("ResearchGroup", back_populates="projects")
    creator: Mapped["User"] = relationship(
        "User", back_populates="created_projects", foreign_keys=[created_by]
    )
    participants: Mapped[list["ProjectParticipant"]] = relationship(
        "ProjectParticipant", back_populates="project", cascade="all, delete-orphan"
    )
    applications: Mapped[list["ProjectApplication"]] = relationship(
        "ProjectApplication", back_populates="project", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
    resources: Mapped[list["ProjectResource"]] = relationship(
        "ProjectResource", back_populates="project", cascade="all, delete-orphan"
    )
