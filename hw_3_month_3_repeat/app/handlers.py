from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards import start_keyboard, keyboard_open_site

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name}!", reply_markup=start_keyboard)
    
    
@router.message(F.text == "Помощьℹ")
async def keyboard_help(message: types.Message):
    await message.answer("Нажмите на команду  /help")
    
    
@router.message(F.text == "Контакты📞")
async def keyboard_help(message: types.Message):
    await message.answer("Вот наши контакты👇\n\n📞  0999464661\n📞  0220521291")
    
    
@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Вот наши комманды👇\n\n/start - Это комманда запускает бота🚀.\n/help - Это комманда выводит все наши комманды👨‍💻.\n/contacts - Это комманда выводит наши контакты📞.", reply_markup=keyboard_open_site)
    

@router.message(Command("contacts"))
async def contacts(message: types.Message):
    await message.answer("Вот наши контакты👇\n\n📞  0999464661\n📞  0220521291")