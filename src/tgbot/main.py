import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from tgbot.config import load_config
from tgbot.db.base import close_db, init_db
from tgbot.handlers.admin import router as admin_router
from tgbot.handlers.errors import router as error_router
from tgbot.handlers.user import router as user_router
from tgbot.middlewares.db_session import DbSessionMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config("/app/.env")

    init_db(config)

    storage = MemoryStorage() if not config.tg_bot.use_redis else RedisStorage.from_url(config.redis.dsn())
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=storage)

    # Регистрируем middleware
    dp.message.middleware(RoleMiddleware(admin_ids=config.tg_bot.admin_ids))
    dp.message.middleware(DbSessionMiddleware())
    dp.message.middleware(ThrottlingMiddleware())

    # Регистрируем роуты
    dp.include_router(admin_router)
    dp.include_router(error_router)
    dp.include_router(user_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot crashed with exception: {e}", exc_info=True)
    finally:
        await close_db()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())