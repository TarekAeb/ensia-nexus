from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class ProjectParticipant(Base):
    __tablename__ = "project_participants"
    __table_args__ = (
        PrimaryKeyConstraint("project_id", "user_id"),
        CheckConstraint(
            "participant_role IN ('MEMBER','REVIEWER','OBSERVER','LEAD')",
            name="project_participants_role_check",
        ),
    )

    project_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    participant_role: Mapped[str] = mapped_column(String(20), nullable=False, default="MEMBER")
    joined_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    project: Mapped["Project"] = relationship("Project", back_populates="participants")
    user: Mapped["User"] = relationship("User", back_populates="project_participations")
