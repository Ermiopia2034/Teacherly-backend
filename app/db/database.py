from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Create async engine for the database
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    # Use connection pooling in production, disable for testing
    poolclass=NullPool if settings.TEST_DATABASE_URL else None,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that yields a SQLAlchemy AsyncSession.
    
    This should be used as a FastAPI dependency to get a database session
    for each request, ensuring proper session lifecycle management.
    
    Yields:
        AsyncSession: SQLAlchemy async session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
