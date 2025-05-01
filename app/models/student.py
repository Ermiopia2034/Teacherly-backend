from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.core.security import encrypt_data, decrypt_data

class Student(Base):
    """
    Student model representing learners in the system.
    
    Contains basic student information and links to grades, attendance, and reports.
    Sensitive data like parent_email is handled with encryption during CRUD operations.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    # parent_email will be encrypted/decrypted during CRUD operations
    # using the security module's encrypt_data/decrypt_data functions
    parent_email = Column(String, unique=False, index=True, nullable=True)
    grade_level = Column(String, nullable=True) # e.g., "Grade 11"

    # Relationships (one-to-many)
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="student", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"
