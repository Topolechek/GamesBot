from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Any, Dict
from tgbot.models.role import UserRole
import logging

logger = logging.getLogger(__name__)

class RoleMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        role = UserRole.ADMIN if user_id in self.admin_ids else UserRole.USER
        data["role"] = role
        logger.debug(f"Set role for user_id={user_id}: {role}")
        return await handler(event, data)