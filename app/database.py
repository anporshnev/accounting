from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings


engine = create_async_engine(settings.db_settings.db_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with async_session_maker() as session:
        yield session