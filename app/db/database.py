from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.config import settings

DATABASE_URL_ASYNC = settings.get_db_url_async()
DATABASE_URL_SYNC = settings.get_db_url_sync()


engine = create_async_engine(url=DATABASE_URL_ASYNC)
async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
