from aiogram import types, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.keyboards import start_keyboard, confirm_order


router = Router()


class Orders(StatesGroup):
    product = State()
    address = State()
    number = State()
    


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.first_name}!", reply_markup=start_keyboard)
    
    
@router.message(F.text == "Заказать🚚")
async def order(message: types.Message, state: FSMContext):
    await message.answer("Введите название товара")
    await state.set_state(Orders.product)
    
    
@router.message(Orders.product)
async def product(message: types.Message, state: FSMContext):
    await state.update_data(product=message.text)
    await message.answer("Укажите ваш адрес")
    await state.set_state(Orders.address)
    
    
@router.message(Orders.address)
async def address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Введите номер телефона")
    await state.set_state(Orders.number)
    
    
@router.message(Orders.number)
async def number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    product = data['product']
    address = data['address']
    number = data['number']
    await message.answer(f"Подтвердите заказ!!!\nТовар - {product}\nАдрес - {address}\nНомер телефона - {number}", reply_markup=confirm_order)
    
    
@router.callback_query(F.data == "confirm")
async def confirm(callback: types.CallbackQuery):
    await callback.message.edit_text("Ваш заказ оформлен.✅\n\nСпасибо за заказ!😊")
    
    
@router.callback_query(F.data == "cancel")
async def cancel(callback: types.CallbackQuery):
    await callback.message.edit_text("Заказ отменён!❌")