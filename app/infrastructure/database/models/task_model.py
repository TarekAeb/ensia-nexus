from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text)
    status = Column(String(15), nullable=False, default='TODO')
    priority = Column(String(10), nullable=False, default='MEDIUM')
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    due_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('TODO','IN_PROGRESS','BLOCKED','DONE','CANCELLED')", name="check_task_status"),
        CheckConstraint("priority IN ('LOW','MEDIUM','HIGH','URGENT')", name="check_task_priority"),
    )

    project = relationship("Project", back_populates="tasks")
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assignee_user_id])

    updates = relationship("TaskUpdate", back_populates="task", cascade="all, delete-orphan")
