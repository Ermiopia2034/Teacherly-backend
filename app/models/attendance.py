import enum
from sqlalchemy import Column, Integer, Date, ForeignKey, Enum as DBEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class AttendanceStatus(str, enum.Enum):
    """
    Enum for attendance status values.
    """
    present = "present"
    absent = "absent"

class Attendance(Base):
    """
    Attendance model for tracking student presence.
    
    Records whether a student was present or absent on a specific date.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)  # Use Date type for just the date
    status = Column(DBEnum(AttendanceStatus), nullable=False)

    # Relationship back to Student
    student = relationship("Student", back_populates="attendance_records")

    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, date='{self.date}', status='{self.status.value}')>"
