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





tovars_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Apple iPhone 16 Pro Max 256GB",callback_data="iphone")],
        [InlineKeyboardButton(text = "Samsung Galaxy Z Fold 6 5G 12+512Gb", callback_data="samsung")],
        [InlineKeyboardButton(text = "Xiaomi 14T 12/256GB", callback_data="mi")]
    ]
)


confirm_cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Подтвердить заказ✅", callback_data="confirm"), InlineKeyboardButton(text = "Отменить заказ❌", callback_data="cancel")]
    ]
)