from sqlalchemy import BigInteger, CheckConstraint, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('TODO','IN_PROGRESS','BLOCKED','DONE','CANCELLED')",
            name="tasks_status_check",
        ),
        CheckConstraint(
            "priority IN ('LOW','MEDIUM','HIGH','URGENT')",
            name="tasks_priority_check",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(15), nullable=False, default="TODO")
    priority: Mapped[str] = mapped_column(String(10), nullable=False, default="MEDIUM")
    created_by: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    assignee_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    creator: Mapped["User"] = relationship(
        "User", back_populates="created_tasks", foreign_keys=[created_by]
    )
    assignee: Mapped["User"] = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_user_id]
    )
    updates: Mapped[list["TaskUpdate"]] = relationship(
        "TaskUpdate", back_populates="task", cascade="all, delete-orphan"
    )
