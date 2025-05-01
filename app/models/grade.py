from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Grade(Base):
    """
    Grade model for storing student assessment results.
    
    Links a student to a specific content item (quiz/exam) with their score and feedback.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    # Links specifically to a Content item (which should be a QuizExam type)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, index=True)
    # Score will be handled with appropriate access controls
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)  # AI generated feedback
    grading_date = Column(DateTime(timezone=True), server_default=func.now())
    # NOTE: extracted_text from OCR is transient and should NOT be stored here.
    # It's handled in the service layer during the grading process.

    # Relationships
    student = relationship("Student", back_populates="grades")
    content = relationship("Content", back_populates="grades")

    def __repr__(self):
        return f"<Grade(id={self.id}, student_id={self.student_id}, content_id={self.content_id}, score={self.score})>"
