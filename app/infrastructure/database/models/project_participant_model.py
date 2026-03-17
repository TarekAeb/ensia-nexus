from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProjectParticipant(Base):
    __tablename__ = "project_participants"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    participant_role = Column(String(20), nullable=False, default='MEMBER')
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("participant_role IN ('MEMBER','REVIEWER','OBSERVER','LEAD')",
                        name="check_project_participant_role"),
    )

    project = relationship("Project", back_populates="participants")
    user = relationship("User")
