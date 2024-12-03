from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Отправить сообщения💬")]
    ],
    resize_keyboard=True, one_time_keyboard=True
)


sender_message_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Отправить✅", callback_data="send")]
    ]
)