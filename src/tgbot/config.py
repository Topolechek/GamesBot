from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@dataclass
class RedisConfig:
    host: str
    port: int
    db: int

    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

@dataclass
class PostgresConfig:
    user: str
    password: str
    host: str
    port: int
    database: str

    def dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    api_keys: dict[str, str]

@dataclass
class Config:
    tg_bot: TgBot
    redis: Optional[RedisConfig] = None
    postgres: Optional[PostgresConfig] = None

def load_config(path: str | Path = ".env") -> Config:
    load_dotenv(path)
    logger.info(f"Loaded .env from {path}")

    bot_token = os.getenv("BOT_TOKEN")
    admin_ids = os.getenv("ADMIN_IDS")
    use_redis = os.getenv("USE_REDIS", "false").lower() == "true"
    steam_api_key = os.getenv("STEAM_API_KEY", "")

    if not bot_token:
        raise ValueError("BOT_TOKEN is not set in .env")
    if not admin_ids:
        raise ValueError("ADMIN_IDS is not set in .env")

    return Config(
        tg_bot=TgBot(
            token=bot_token,
            admin_ids=[int(x) for x in admin_ids.split(",")],
            use_redis=use_redis,
            api_keys={"steam": steam_api_key},
        ),
        redis=(
            RedisConfig(
                host=os.getenv("REDIS_HOST"),
                port=int(os.getenv("REDIS_PORT")),
                db=int(os.getenv("REDIS_DB")),
            )
            if use_redis
            else None
        ),
        postgres=PostgresConfig(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=int(os.getenv("POSTGRES_PORT")),
            database=os.getenv("POSTGRES_DATABASE"),
        ),
    )