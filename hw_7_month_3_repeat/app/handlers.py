import asyncio
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.keyboards import start_keyboard, confirm_keyboards
from app.db import conn, cursor
from config import token
from aiogram import Bot
from datetime import datetime
import aioschedule, logging
from aiogram.exceptions import TelegramBadRequest

router = Router() 
bot = Bot(token=token)

# Состояния для FSM
class Users(StatesGroup):
    full_name = State()
    age = State()
    phone = State()
    schedules = State()
    deadline = State()


users_data = {}
# Глобальный словарь для планирования задач
scheduled_tasks = {}


# Команда /start
@router.message(CommandStart())
async def start(message: Message):
    users_data['chat_id'] = message.chat.id
    await message.answer(f"Привет {message.from_user.first_name}, пройдите регистрацию!", reply_markup=start_keyboard)


@router.callback_query(F.data == "register")
async def register(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите ФИО")
    await state.set_state(Users.full_name)


@router.message(Users.full_name)
async def full_name_(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите ваш возраст")
    await state.set_state(Users.age)


@router.message(Users.age)
async def age_(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите номер телефона")
    await state.set_state(Users.phone)


@router.message(Users.phone)
async def phone_(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    full_name = data['full_name']
    age = data['age']
    phone = data['phone']
    await message.answer(f"Подтвердите ваши данные!\n\nФИО - {full_name}.\nВозраст - {age}.\nНомер телефона - {phone}.", reply_markup=confirm_keyboards)


@router.callback_query(lambda callback: callback.data in {"confirm", "cancel"})
async def confirm_(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "confirm":
        data = await state.get_data()
        full_name = data['full_name']
        age = data['age']
        phone = data['phone']
        chat_id = callback.message.chat.id
        cursor.execute("INSERT INTO users (id, full_name, age, phone, chat_id) VALUES (?, ?, ?, ?, ?)", (callback.message.from_user.id, full_name, age, phone, chat_id))
        conn.commit()
        await state.clear()
        await callback.message.answer("Вы успешно зарегистрировались ✅")
    elif callback.data == "cancel":
        await state.clear()
        await callback.message.answer("Отменено ❌")



@router.message(Command("set_schedule"))
async def set_schedule(message: Message):
    await message.answer("Введите время для получения уведомления в формате ДД.ММ.ГГГГ ЧЧ:ММ (например, 09.12.2024 13:30):")


@router.message()
async def handle_time_input(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_input = message.text.strip()

    try:
        # Парсим дату и время в формате "ДД.ММ.ГГГГ ЧЧ:ММ"
        schedule_time = datetime.strptime(user_input, "%d.%m.%Y %H:%M")

        now = datetime.now()

        # Если время в будущем, то продолжаем
        if schedule_time <= now:
            await message.answer("Время должно быть в будущем. Попробуйте снова.")
            return

        # Сохраняем в базу данных
        cursor.execute("""
            UPDATE users 
            SET chat_id = ?, time_schedule = ?
            WHERE id = ?
        """, (chat_id, user_input, user_id))

        # Сохраняем изменения
        conn.commit()

        await message.answer(f"Ваше уведомление установлено на {user_input}.")

        # Преобразуем время в формат HH:MM для aioschedule
        time_to_notify = schedule_time.strftime("%H:%M")

        # Планируем задачу с использованием aioschedule
        aioschedule.every().day.at(time_to_notify).do(notify_user, chat_id)

    except ValueError:
        # Сообщаем пользователю об ошибке формата
        await message.answer("Неверный формат. Пожалуйста, используйте формат 'ДД.ММ.ГГГГ ЧЧ:ММ' (например, 09.12.2024 13:30).")


logging.basicConfig(level=logging.DEBUG)

async def notify_user(chat_id):
    logging.debug(f"Отправка уведомления пользователю {chat_id}")
    await bot.send_message(chat_id, "Пора выполнить задачу!")







