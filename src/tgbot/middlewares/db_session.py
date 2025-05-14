from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Any, Dict

from tgbot.db.base import get_db


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        async for session in get_db():
            data["session"] = session
            return await handler(event, data)