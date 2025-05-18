import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import URL
from tgbot.config.secrets import ENV

import logging

logger = logging.getLogger(__name__)

# class Base(DeclarativeBase):
#     pass

DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    username=ENV.get("POSTGRES_USER"),
    password=ENV.get("POSTGRES_PASSWORD"),
    host=ENV.get("POSTGRES_HOST"),
    port=ENV.get("POSTGRES_PORT"),
    database=ENV.get("POSTGRES_DB"),
)

DATABASE_PARAMS = {
    "pool_pre_ping": True,
    "echo": False,
    "pool_size": 10,
    "max_overflow": 50,
}


engine = create_async_engine(
    DATABASE_URL,
    **DATABASE_PARAMS,
    json_serializer=json.dumps,
    json_deserializer=json.loads,
)
DBSession = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def close_db():
    global engine
    if engine:
        await engine.dispose()
        logger.info("Database engine disposed")

async def get_db() -> AsyncSession:
    if DBSession is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    async with DBSession() as session:
        try:
            yield session
        finally:
            await session.close()