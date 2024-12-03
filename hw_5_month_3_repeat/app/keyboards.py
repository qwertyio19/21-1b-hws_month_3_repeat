from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Заказать🚚")]
    ],
    resize_keyboard=True
)


confirm_order = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Подтвердить✅", callback_data="confirm")], [InlineKeyboardButton(text = "Отменить❌", callback_data="cancel")]
    ]
)