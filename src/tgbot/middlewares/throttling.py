import asyncio
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 0.5):
        self.limit = limit
        self.last_call: dict[int, float] = {}
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        current_time = asyncio.get_event_loop().time()

        if user_id in self.last_call:
            if current_time - self.last_call[user_id] < self.limit:
                await event.answer("Please wait a moment before sending another command.")
                return
        self.last_call[user_id] = current_time
        return await handler(event, data)