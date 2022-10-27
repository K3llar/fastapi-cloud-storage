from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.database_url,
                             echo=True,
                             future=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        yield async_session
