from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from tgbot.filters.role import AdminFilter

router = Router()

@router.message(AdminFilter(is_admin=True), Command(commands=["admin"]))
async def admin_command(message: Message):
    await message.answer("This is an admin-only command!")

@router.message(AdminFilter(is_admin=True), Command(commands=["start"]))
async def cmd_start(message: Message):
    try:
        await message.answer("Welcome admin")
    except Exception as e:
        print(f"Error in cmd_start: {e}")
        raise