from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    experience_years = Column(Integer, nullable=False, default=0)
    grade = Column(String(20), nullable=False)
    department = Column(Text)
    research_interests = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("experience_years >= 0", name="check_experience_years"),
        CheckConstraint("grade IN ('MCA','PROFESSOR','DOCTOR','ADMIN')", name="check_teacher_grade"),
    )

    user = relationship("User", back_populates="teacher_profile")

    # Relationships
    managed_labs = relationship("ResearchLab", back_populates="head_teacher")
    led_groups = relationship("ResearchGroup", back_populates="leader")
