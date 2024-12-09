from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Регистрация", callback_data="register")]
    ]
)


confirm_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Подтвердить✅", callback_data="confirm")], [InlineKeyboardButton(text = "Отменить❌", callback_data="cancel")]
    ]
)





