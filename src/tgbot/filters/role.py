from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Union, Collection, Set, Optional, Dict, Any
import logging

from tgbot.models.role import UserRole

logger = logging.getLogger(__name__)


class RoleFilter(BaseFilter):
    def __init__(
            self,
            role: Union[None, UserRole, Collection[UserRole]] = None,
    ):
        if role is None:
            self.roles: Optional[Set[UserRole]] = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def __call__(self, message: Message, **data: Dict[str, Any]) -> bool:
        if self.roles is None:
            logger.debug("No roles specified, allowing all roles")
            return True

        role = data.get("role")
        if role is None:
            logger.warning("Role not found in context data: %s", data)
            return False

        is_role_matched = role in self.roles
        logger.debug(f"Role check: user_role={role}, required_roles={self.roles}, result={is_role_matched}")
        return is_role_matched


class AdminFilter(BaseFilter):
    def __init__(self, is_admin: Optional[bool] = None):
        self.is_admin = is_admin

    async def __call__(self, message: Message, **data: Dict[str, Any]) -> bool:
        if self.is_admin is None:
            logger.debug("is_admin not specified, allowing all")
            return True

        role = data.get("role")
        if role is None:
            logger.warning("Role not found in context data: %s", data)
            return False

        is_admin_user = (role is UserRole.ADMIN)
        result = (is_admin_user == self.is_admin)
        logger.debug(f"Admin check: user_role={role}, is_admin={self.is_admin}, result={result}")
        return result