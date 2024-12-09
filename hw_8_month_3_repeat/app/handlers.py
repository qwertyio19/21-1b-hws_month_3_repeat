from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.keyboards import start_keyboard, tovars_keyboard, confirm_cancel_keyboard


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name} выбери товары👇", reply_markup=start_keyboard)