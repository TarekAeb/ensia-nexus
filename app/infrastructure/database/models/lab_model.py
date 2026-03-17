from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ResearchLab(Base):
    __tablename__ = "research_labs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    head_teacher_id = Column(Integer, ForeignKey("teachers.user_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    head_teacher = relationship("Teacher", back_populates="managed_labs")
    research_groups = relationship("ResearchGroup", back_populates="lab", cascade="all, delete-orphan")
