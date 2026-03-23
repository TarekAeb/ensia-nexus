from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = (
        CheckConstraint(
            "grade IN ('MCA','PROFESSOR','DOCTOR','ADMIN')",
            name="teachers_grade_check",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    experience_years: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("experience_years >= 0", name="teachers_experience_check"),
        nullable=False,
        default=0,
    )
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    department: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_interests: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="teacher")
    headed_labs: Mapped[list["ResearchLab"]] = relationship(
        "ResearchLab", back_populates="head_teacher", foreign_keys="ResearchLab.head_teacher_id"
    )
    led_groups: Mapped[list["ResearchGroup"]] = relationship(
        "ResearchGroup", back_populates="leader", foreign_keys="ResearchGroup.leader_user_id"
    )
