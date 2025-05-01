import enum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as DBEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class EmailStatus(str, enum.Enum):
    """
    Enum for tracking the status of report emails.
    """
    sent = "sent"
    failed = "failed"
    pending = "pending"
    not_applicable = "not_applicable"  # e.g., for Excel export, not emailed

class Report(Base):
    """ 
    Stores metadata about generated reports (e.g., for tracking email status).
    
    Tracks report generation and delivery status for student performance reports.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    generation_date = Column(DateTime(timezone=True), server_default=func.now())
    email_status = Column(DBEnum(EmailStatus), nullable=True, default=EmailStatus.not_applicable)

    # Relationships
    teacher = relationship("Teacher", back_populates="reports")
    student = relationship("Student", back_populates="reports")

    def __repr__(self):
        return f"<Report(id={self.id}, student_id={self.student_id}, teacher_id={self.teacher_id}, status='{self.email_status.value if self.email_status else None}')>"
