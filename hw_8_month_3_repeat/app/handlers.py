from aiogram import Router, types, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.keyboards import start_keyboard, tovars_keyboard, confirm_cancel_keyboard


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет {message.from_user.first_name} выбери товары👇", reply_markup=start_keyboard)


@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.message.answer("Вот наши товары👇", reply_markup=tovars_keyboard)


@router.callback_query(lambda callback: callback.data in {"iphone", "samsung", "mi"})
async def phones(callback: CallbackQuery):
    if callback.data == "iphone":
        await callback.message.answer_photo("https://ostore.kg/upload/resize_cache/iblock/a0b/500_500_1/a0b8f9411e1e1393ea959508fab9fd1b.png", caption="Товар - Apple iPhone 16 Pro Max 256GB\nЦена - 133990 сом", reply_markup=confirm_cancel_keyboard)

    elif callback.data == "samsung":
        await callback.message.answer_photo("https://www.myphone.kg/cache/files/23789.webp_w800_h800_resize.webp?t=1720879438", caption="Товар - Samsung Galaxy Z Fold 6 5G 12+512Gb\nЦена - 139 990 сом", reply_markup=confirm_cancel_keyboard)

    elif callback.data == "mi":
        await callback.message.answer_photo("https://www.kivano.kg/images/product/141840/173019482024775_full.jpg", caption="Товар - Xiaomi 14T 12/256GB\nЦена - 41740 сом", reply_markup=confirm_cancel_keyboard)


@router.callback_query(lambda callback: callback.data in {"confirm", "cancel"})
async def confirm_cancel(callback: CallbackQuery):
    if callback.data == "confirm":
        await callback.message.answer("Заказ подтверждён✅")

    elif callback.data == "cancel":
        await callback.message.answer("Заказ отменён❌", reply_markup=tovars_keyboard)


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Вот наши команды👇\n/start - запускает бота\n/help - Выводит все команды бота")