from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# This will be implemented later when we set up authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")

# This will be implemented later when we set up the database
def get_db() -> Generator:
    """
    Dependency for getting DB session.
    Will be implemented when database setup is complete.
    """
    try:
        db = None  # Will be replaced with SessionLocal() from database.py
        yield db
    finally:
        if db:
            db.close()

# This will be implemented later when we set up authentication
async def get_current_user():
    """
    Dependency for getting the current authenticated user.
    Will be implemented when authentication is set up.
    """
    pass

# This will be implemented later when we set up authentication
async def get_current_active_user():
    """
    Dependency for getting the current active authenticated user.
    Will be implemented when authentication is set up.
    """
    pass
