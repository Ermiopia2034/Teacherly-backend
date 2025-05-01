from app.db.base_class import Base
from .user import User, UserRole
from .teacher import Teacher
from .student import Student
from .content import Content, QuizExam, TeachingMaterial
from .grade import Grade
from .attendance import Attendance, AttendanceStatus
from .report import Report, EmailStatus

# Expose all models for cleaner imports elsewhere
__all__ = [
    "Base", "User", "UserRole", "Teacher", "Student", "Content", "QuizExam",
    "TeachingMaterial", "Grade", "Attendance", "AttendanceStatus", "Report",
    "EmailStatus"
]