from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        CheckConstraint(
            "level IN ('PHD','UNDERGRADUATE','GRADUATE')",
            name="students_level_check",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    university: Mapped[str | None] = mapped_column(Text, nullable=True)
    level: Mapped[str | None] = mapped_column(Text, nullable=True)
    major: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    research_interests: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    cv_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="student")
    applications: Mapped[list["ProjectApplication"]] = relationship(
        "ProjectApplication", back_populates="student", cascade="all, delete-orphan"
    )
