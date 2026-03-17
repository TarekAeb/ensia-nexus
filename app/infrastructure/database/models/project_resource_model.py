from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ProjectResource(Base):
    __tablename__ = "project_resources"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    resource_type = Column(String(20), nullable=False)
    title = Column(Text, nullable=False)
    url = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("resource_type IN ('PAPER_DOC','GIT_REPO','DATASET','OTHER')", name="check_resource_type"),
    )

    project = relationship("Project", back_populates="resources")
    creator = relationship("User", foreign_keys=[created_by])
