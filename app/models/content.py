from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func  # For default timestamps
from app.db.base_class import Base

class Content(Base):
    """ 
    Base model for all teaching content (materials, quizzes, exams).
    
    This is the parent class for different types of educational content
    using SQLAlchemy's joined table inheritance.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, index=True)
    # Discriminator column for joined table inheritance
    type = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    # Flexible storage for answer key - specific format depends on grading logic
    answer_key = Column(Text, nullable=True)

    # Relationship back to Teacher
    teacher = relationship("Teacher", back_populates="contents")
    # Relationship to Grades (one-to-many)
    grades = relationship("Grade", back_populates="content", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "content",  # Identity of the base class
        "polymorphic_on": type,             # Column defining the subtype
    }

    def __repr__(self):
        return f"<Content(id={self.id}, type='{self.type}', title='{self.title}')>"


class QuizExam(Content):
    """ 
    Model for Quizzes and Exams, inheriting from Content.
    
    Extends the base Content model with quiz/exam specific fields.
    """
    
    __tablename__ = "quiz_exams"

    # Links back to the parent 'contents' table id
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)
    # Store questions (e.g., list of dicts: {'q': '...', 'options': [], 'answer': ...})
    questions = Column(JSON, nullable=True)
    max_score = Column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "quiz_exam",  # Identity for this subtype
    }

    def __repr__(self):
        return f"<QuizExam(id={self.id}, title='{self.title}', max_score={self.max_score})>"


class TeachingMaterial(Content):
    """ 
    Model for Teaching Materials (lesson plans, worksheets), inheriting from Content.
    
    Extends the base Content model with teaching material specific fields.
    """
    
    __tablename__ = "teaching_materials"

    # Links back to the parent 'contents' table id
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)
    material_type = Column(String, nullable=True)  # e.g., "lesson plan", "worksheet"
    content_body = Column(Text, nullable=True)  # The actual text/instructions

    __mapper_args__ = {
        "polymorphic_identity": "teaching_material",  # Identity for this subtype
    }

    def __repr__(self):
        return f"<TeachingMaterial(id={self.id}, title='{self.title}', type='{self.material_type}')>"
