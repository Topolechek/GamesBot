from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import logging
from tgbot.config.secrets import ENV

logger = logging.getLogger(__name__)

@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str | None = None

    def dsn(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

@dataclass
class PostgresConfig:
    user: str
    password: str
    host: str
    port: int
    database: str

    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

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
    logger.info(f"Loaded .env from {path}")

    bot_token = ENV.get("BOT_TOKEN")
    admin_ids = ENV.get("ADMIN_IDS")
    use_redis = ENV.get("USE_REDIS", "false").lower() == "true"
    steam_api_key = ENV.get("STEAM_API_KEY", "")

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
                host=ENV.get("REDIS_HOST"),
                port=int(ENV.get("REDIS_PORT")),
                password=ENV.get("REDIS_PASSWORD"),
                db=int(ENV.get("REDIS_DB")),
            )
            if use_redis
            else None
        ),
        postgres=PostgresConfig(
            user=ENV.get("POSTGRES_USER"),
            password=ENV.get("POSTGRES_PASSWORD"),
            host=ENV.get("POSTGRES_HOST"),
            port=int(ENV.get("POSTGRES_PORT")),
            database=ENV.get("POSTGRES_DATABASE"),
        ),
    )