from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    This class provides common functionality for all models,
    such as automatic table naming based on the class name.
    """
    
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate __tablename__ automatically from the class name.
        Converts CamelCase to snake_case.
        
        For example:
        - UserProfile -> user_profile
        - StudentAssignment -> student_assignment
        """
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in cls.__name__]).lstrip('_')
