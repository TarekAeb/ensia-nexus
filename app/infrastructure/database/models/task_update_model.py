from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class TaskUpdate(Base):
    __tablename__ = "task_updates"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(Text, nullable=False)
    hours_added = Column(Numeric(6, 2), nullable=False, default=0)
    new_status = Column(String(15), nullable=True)
    new_progress = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("new_status IN ('TODO','IN_PROGRESS','BLOCKED','DONE','CANCELLED')",
                        name="check_task_update_status"),
        CheckConstraint("new_progress BETWEEN 0 AND 100", name="check_task_update_progress"),
    )

    task = relationship("Task", back_populates="updates")
    author = relationship("User", foreign_keys=[author_user_id])
