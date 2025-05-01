from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Get a user by ID.
    
    Args:
        db: Database session
        user_id: ID of the user to retrieve
        
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by email.
    
    Args:
        db: Database session
        email: Email of the user to retrieve
        
    Returns:
        User object if found, None otherwise
    """
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_users(
    db: AsyncSession, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None
) -> list[User]:
    """
    Get a list of users with optional role filtering.
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        role: Optional role filter
        
    Returns:
        List of User objects
    """
    query = select(User)
    if role:
        query = query.filter(User.role == role)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db: Database session
        user_in: User creation data
        
    Returns:
        Created User object
    """
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(
    db: AsyncSession, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """
    Update a user.
    
    Args:
        db: Database session
        db_user: Existing user object to update
        user_in: User update data
        
    Returns:
        Updated User object
    """
    user_data = user_in.model_dump() if hasattr(user_in, "model_dump") else user_in
    
    if "password" in user_data and user_data["password"]:
        hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password
        
    for field, value in user_data.items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)
            
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Delete a user.
    
    Args:
        db: Database session
        user_id: ID of the user to delete
        
    Returns:
        Deleted User object if found, None otherwise
    """
    user = await get_user(db, user_id=user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user with email and password.
    
    Args:
        db: Database session
        email: User email
        password: Plain text password
        
    Returns:
        User object if authentication is successful, None otherwise
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"Authentication attempt for email: {email}")
    
    user = await get_user_by_email(db, email=email)
    if not user:
        logger.warning(f"Authentication failed: No user found with email {email}")
        return None
        
    logger.info(f"User found, verifying password for user ID: {user.id}")
    password_valid = verify_password(password, user.hashed_password)
    
    if not password_valid:
        logger.warning(f"Authentication failed: Invalid password for user {email}")
        return None
        
    logger.info(f"Authentication successful for user {email}")
    return user
