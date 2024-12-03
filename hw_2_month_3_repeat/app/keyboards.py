from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text = "Автозапчасти🚗", callback_data="auto_parts")],
        [InlineKeyboardButton(text = "Мобильные запчасти📱", callback_data="mobile_spare_parts")]
    ],
    
)