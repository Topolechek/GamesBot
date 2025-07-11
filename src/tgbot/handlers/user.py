from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    try:
        await message.answer("Welcome")
    except Exception as e:
        print(f"Error in cmd_start: {e}")
        raise