from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Помощьℹ")], [KeyboardButton(text = "Контакты📞")]
    ], 
    resize_keyboard=True, one_time_keyboard=True
)


keyboard_open_site = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Открыть сайт", url="https://24.kg/")]
    ]
)