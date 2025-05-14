from aiogram import Router
from aiogram.types import ErrorEvent
from aiogram.exceptions import TelegramAPIError

router = Router()

# @router.error()
# async def error_handler(event: ErrorEvent):
#     if isinstance(event.exception, TelegramAPIError):
#         await event.update.message.answer("An error occurred with Telegram API.")
#     else:
#         await event.update.message.answer("An unexpected error occurred.")