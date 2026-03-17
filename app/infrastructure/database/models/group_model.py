from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResearchGroup(Base):
    __tablename__ = "research_groups"

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("research_labs.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text)
    leader_user_id = Column(Integer, ForeignKey("teachers.user_id"), nullable=False)
    is_validated = Column(Boolean, nullable=False, default=False)
    validated_by_admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    lab = relationship("ResearchLab", back_populates="research_groups")
    leader = relationship("Teacher", back_populates="led_groups")
    validated_by_admin = relationship("User", foreign_keys=[validated_by_admin_id])

    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="group", cascade="all, delete-orphan")
