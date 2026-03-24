from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False) # RESEARCH, ADMIN, EVENT
    tags = Column(String, nullable=True) # Comma-separated tags
    author_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", backref="announcements")

class AnnouncementComment(Base):
    __tablename__ = "announcement_comments"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", backref="announcement_comments")
    announcement = relationship("Announcement", backref="comments")

class AnnouncementReaction(Base):
    __tablename__ = "announcement_reactions"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reaction_type = Column(String, nullable=False) # like, celebrate, insightful, etc.

    user = relationship("User", backref="announcement_reactions")
    announcement = relationship("Announcement", backref="reactions")
