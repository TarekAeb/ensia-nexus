from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class ProjectApplication(Base):
    __tablename__ = "project_applications"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING','ACCEPTED','REJECTED')",
            name="project_applications_status_check",
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    student_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("students.user_id", ondelete="CASCADE"), nullable=False
    )
    motivation: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="PENDING")
    reviewed_by: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    reviewed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    decision_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    project: Mapped["Project"] = relationship("Project", back_populates="applications")
    student: Mapped["Student"] = relationship("Student", back_populates="applications")
    reviewer: Mapped["User"] = relationship(
        "User", back_populates="reviewed_applications", foreign_keys=[reviewed_by]
    )
