import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as DBEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class UserRole(str, enum.Enum):
    teacher = "teacher"
    admin = "admin"

class User(Base):
    """
    User model for authentication and authorization.
    
    Represents a user in the system with role-based access control.
    """
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(DBEnum(UserRole), nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    # Relationship to Teacher (one-to-one)
    # cascade="all, delete-orphan": ensures Teacher is deleted if User is deleted
    teacher = relationship(
        "Teacher",
        back_populates="user",
        uselist=False, # Indicates one-to-one
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"
