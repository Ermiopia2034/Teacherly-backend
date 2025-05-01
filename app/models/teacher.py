from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Teacher(Base):
    """
    Teacher model representing educators in the system.
    
    Contains professional details and links to a User account for authentication.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    # unique=True enforces the one-to-one relationship with User at DB level
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, index=True)
    school = Column(String, nullable=True)
    grade_levels_taught = Column(String, nullable=True) # e.g., "Grade 10-12"
    subject = Column(String, index=True, nullable=True) # e.g., "Physics"

    # Relationship back to User
    user = relationship("User", back_populates="teacher")

    # Relationships to Content and Report (one-to-many)
    # cascade: ensures related Contents/Reports are deleted if Teacher is deleted
    contents = relationship("Content", back_populates="teacher", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="teacher", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Teacher(id={self.id}, name='{self.name}', user_id={self.user_id})>"
