from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class ResearchGroup(Base):
    __tablename__ = "research_groups"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    lab_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("research_labs.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    leader_user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("teachers.user_id"), nullable=True
    )
    is_validated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    validated_by_admin_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    validated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    lab: Mapped["ResearchLab"] = relationship("ResearchLab", back_populates="groups")
    leader: Mapped["Teacher"] = relationship(
        "Teacher", back_populates="led_groups", foreign_keys=[leader_user_id]
    )
    validator: Mapped["User"] = relationship(
        "User", back_populates="validated_groups", foreign_keys=[validated_by_admin_id]
    )
    members: Mapped[list["GroupMember"]] = relationship(
        "GroupMember", back_populates="group", cascade="all, delete-orphan"
    )
    projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="group", cascade="all, delete-orphan"
    )
