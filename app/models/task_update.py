from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class TaskUpdate(Base):
    __tablename__ = "task_updates"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    author_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    hours_added: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False, default=0)
    new_status: Mapped[str | None] = mapped_column(String(15), nullable=True)
    new_progress: Mapped[int | None] = mapped_column(
        Integer,
        CheckConstraint("new_progress >= 0 AND new_progress <= 100", name="task_updates_progress_check"),
        nullable=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    task: Mapped["Task"] = relationship("Task", back_populates="updates")
    author: Mapped["User"] = relationship(
        "User", back_populates="task_updates", foreign_keys=[author_user_id]
    )
