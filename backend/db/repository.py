from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.config.settings import settings
import logging

logger = logging.getLogger("resumeiq.db")

# Create Async Engine for PostgreSQL
try:
    engine = create_async_engine(
        settings.async_database_url,
        echo=False,
    )
    # Session factory
    AsyncSessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
except Exception as e:
    logger.error(f"Failed to initialize database engine: {e}")
    engine = None
    AsyncSessionLocal = None

Base = declarative_base()

async def get_db():
    """Dependency injection for database sessions."""
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized")
        
    async with AsyncSessionLocal() as session:
        yield session
