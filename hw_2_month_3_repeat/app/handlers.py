from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.keyboards import start_inline_keyboard

router = Router()

AUTO_PARTS = {
    "Аккумуляторная батарея Varta": 16481,
    "Барабан тормозной TRIALLI": 7820,
    "Подшипник опоры передней стойки": 1273,
}

MOBILE_SPARE_PARTS = {
    "Сенсор+дисплей Google pixel 3": 8000,
    "Сенсор+дисплей OnePlus 5T": 6000,
    "Сенсор+дисплей Zte Nubia Red Magic 6 Pro": 15000,
}

orders = {}

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name}", reply_markup=start_inline_keyboard)

@router.callback_query(F.data == "auto_parts")
async def auto_parts(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for autoparts, price in AUTO_PARTS.items():
        builder.button(
            text=f"{autoparts} - {price} сом",
            callback_data=f"auto_{autoparts}"
        )
    builder.adjust(1)
    await callback.message.answer("Меню автозапчастей:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("auto_"))
async def choise_auto_parts(callback: types.CallbackQuery):
    autoparts = callback.data[len("auto_"):].strip()
    orders[callback.from_user.id] = {"autoparts": autoparts, "quantity": 1}

    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        builder.button(
            text=str(i),
            callback_data=f"quantity_auto_{i}"
        )
    builder.adjust(2)
    await callback.message.edit_text(f"Вы выбрали {autoparts}.\nУкажите количество:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("quantity_auto_"))
async def quantity_auto(callback: types.CallbackQuery):
    quantity = int(callback.data[len("quantity_auto_"):])
    user_id = callback.from_user.id

    if user_id in orders and "autoparts" in orders[user_id]:
        orders[user_id]["quantity"] = quantity
        autoparts = orders[user_id]["autoparts"]
        price = AUTO_PARTS[autoparts] * quantity

        builder = InlineKeyboardBuilder()
        builder.button(
            text="Подтвердить заказ✅",
            callback_data="confirm_auto_order"
        )
        await callback.message.edit_text(
            f"Ваш заказ: {autoparts} \nКоличество: {quantity}\nИтого: {price} сом.",
            reply_markup=builder.as_markup()
        )

@router.callback_query(F.data == 'confirm_auto_order')
async def confirm_auto_order(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in orders and "autoparts" in orders[user_id]:
        autoparts = orders[user_id]['autoparts']
        quantity = orders[user_id]['quantity']
        total_price = AUTO_PARTS[autoparts] * quantity

        del orders[user_id]
        await callback.message.edit_text(
            f"Спасибо за заказ!😊\nВы заказали: {autoparts} \nКоличество: {quantity}.\nИтого к оплате: {total_price} сом."
        )

@router.callback_query(F.data == "mobile_spare_parts")
async def mobile_spare_parts(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for mobileparts, price in MOBILE_SPARE_PARTS.items():
        builder.button(
            text=f"{mobileparts} - {price} сом",
            callback_data=f"mobile_{mobileparts}"
        )
    builder.adjust(1)
    await callback.message.answer("Меню мобильных запчастей:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("mobile_"))
async def choise_mobile_parts(callback: types.CallbackQuery):
    mobileparts = callback.data[len("mobile_"):].strip()
    orders[callback.from_user.id] = {"mobileparts": mobileparts, "quantity": 1}

    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        builder.button(
            text=str(i),
            callback_data=f"quantity_mobile_{i}"
        )
    builder.adjust(2)
    await callback.message.edit_text(f"Вы выбрали {mobileparts}. Укажите количество:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("quantity_mobile_"))
async def quantity_mobile(callback: types.CallbackQuery):
    quantity = int(callback.data[len("quantity_mobile_"):])
    user_id = callback.from_user.id

    if user_id in orders and "mobileparts" in orders[user_id]:
        orders[user_id]["quantity"] = quantity
        mobileparts = orders[user_id]["mobileparts"]
        price = MOBILE_SPARE_PARTS[mobileparts] * quantity

        builder = InlineKeyboardBuilder()
        builder.button(
            text="Подтвердить заказ✅",
            callback_data="confirm_mobile_order"
        )
        await callback.message.edit_text(
            f"Ваш заказ: {mobileparts} \nКоличество: {quantity}\nИтого: {price} сом.",
            reply_markup=builder.as_markup()
        )

@router.callback_query(F.data == 'confirm_mobile_order')
async def confirm_mobile_order(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in orders and "mobileparts" in orders[user_id]:
        mobileparts = orders[user_id]['mobileparts']
        quantity = orders[user_id]['quantity']
        total_price = MOBILE_SPARE_PARTS[mobileparts] * quantity

        del orders[user_id]
        await callback.message.edit_text(
            f"Спасибо за заказ!😊\nВы заказали: {mobileparts} \nКоличество: {quantity}.\nИтого к оплате: {total_price} сом."
        )