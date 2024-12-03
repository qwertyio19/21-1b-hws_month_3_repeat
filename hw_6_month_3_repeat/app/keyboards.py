from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить сообщение✉️", callback_data="message"),
            InlineKeyboardButton(text="Отправить фото📸", callback_data="photo"),
        ],
        [
            InlineKeyboardButton(text="Отправить видео🎬", callback_data="video"),
            InlineKeyboardButton(text="Отправить аудио🎵", callback_data="audio"),
        ],
    ]
)


confirm_keyboards = {
    "message": InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text = "Отправить✅", callback_data="confirm_message"),
                          InlineKeyboardButton(text = "Отменить❌", callback_data="cancel_message")]]
    ),
    "photo": InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text = "Отправить✅", callback_data="confirm_photo"),
                          InlineKeyboardButton(text = "Отменить❌", callback_data="cancel_photo")]]
    ),
    "video": InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text = "Отправить✅", callback_data="confirm_video"),
                          InlineKeyboardButton(text = "Отменить❌", callback_data="cancel_video")]]
    ),
    "audio": InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text = "Отправить✅", callback_data="confirm_audio"),
                          InlineKeyboardButton(text = "Отменить❌", callback_data="cancel_audio")]]
    ),
}