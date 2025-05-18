import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from tgbot.db.base import close_db
from tgbot.handlers.admin import router as admin_router
from tgbot.handlers.errors import router as error_router
from tgbot.handlers.user import router as user_router
from tgbot.middlewares.db_session import DbSessionMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.config.secrets import ENV
from tgbot.config_file import RedisConfig

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    if ENV.get("USE_REDIS"):
        redis_conf = RedisConfig(
            host=ENV.get("REDIS_HOST"),
            port=int(ENV.get("REDIS_PORT", 0)),
            db=int(ENV.get("REDIS_DB", 0)),
            password=ENV.get("REDIS_PASSWORD") or None,
        )
        storage = RedisStorage.from_url(redis_conf.dsn())
    else:
        storage = MemoryStorage()

    bot = Bot(token=ENV.get("BOT_TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)

    main_router = Router()
    main_router.message.middleware(RoleMiddleware(admin_ids=ENV.get("ADMIN_IDS")))
    main_router.message.middleware(DbSessionMiddleware())
    main_router.message.middleware(ThrottlingMiddleware())
    main_router.include_router(admin_router)
    main_router.include_router(error_router)
    main_router.include_router(user_router)

    dp.include_router(main_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot crashed with exception: {e}", exc_info=True)
    finally:
        await close_db()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())