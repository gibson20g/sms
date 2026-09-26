import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# If running tests or sqlite fallback
db_url = settings.DATABASE_URL
if os.environ.get("TESTING") == "1" or db_url.startswith("sqlite"):
    if not db_url.startswith("sqlite+aiosqlite"):
        db_url = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(db_url, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
