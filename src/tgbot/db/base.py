import json
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import logging

from tgbot.config import Config, load_config

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

DATABASE_PARAMS = {
    "pool_pre_ping": True,
    "echo": False,
    "pool_size": 10,
    "max_overflow": 50,
}

engine = None
DBSession = None

def init_db(config: Config):
    global engine, DBSession
    if engine is None:
        engine = create_async_engine(
            config.postgres.dsn(),
            **DATABASE_PARAMS,
            json_serializer=json.dumps,
            json_deserializer=json.loads,
        )
        DBSession = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.info("Database engine initialized")

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