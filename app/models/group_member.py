from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class GroupMember(Base):
    __tablename__ = "group_members"
    __table_args__ = (
        PrimaryKeyConstraint("group_id", "user_id"),
    )

    group_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("research_groups.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    joined_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    group: Mapped["ResearchGroup"] = relationship("ResearchGroup", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="group_memberships")
