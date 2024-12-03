from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_keyboard = ReplyKeyboardMarkup(
    keyboard= [
        [KeyboardButton(text = "Новости🗞")],
        [KeyboardButton(text = "Курсы валют💹")],
        [KeyboardButton(text = "Контактная информацияℹ")],
        [KeyboardButton(text = "Часто задаваемые вопросы❓")]
    ],
    resize_keyboard=True
)