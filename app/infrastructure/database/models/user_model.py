from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)
    institution = Column(Text)
    department = Column(Text)
    contact_email = Column(Text)
    phone_number = Column(Text)
    address = Column(Text)
    website = Column(Text)
    password_hash = Column(Text)  # if null -> user is created via GOOGLE and cannot login with password
    email_verified = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("role IN ('STUDENT', 'TEACHER', 'ADMIN')", name="check_user_role"),
    )

    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")
