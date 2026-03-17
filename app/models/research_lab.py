from sqlalchemy import BigInteger, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class ResearchLab(Base):
    __tablename__ = "research_labs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    head_teacher_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.user_id"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    head_teacher: Mapped["Teacher"] = relationship(
        "Teacher", back_populates="headed_labs", foreign_keys=[head_teacher_id]
    )
    groups: Mapped[list["ResearchGroup"]] = relationship(
        "ResearchGroup", back_populates="lab", cascade="all, delete-orphan"
    )
