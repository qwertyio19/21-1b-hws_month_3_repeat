from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import smtplib
import logging
import re
from email.message import EmailMessage
from config import smtp_sender, smtp_password
from app.db import cursor, conn
from app.keyboards import start_keyboard, sender_message_keyboard


def is_valid_email(email: str) -> bool:
    """Проверяет, является ли строка корректным email."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def is_non_empty_text(text: str) -> bool:
    """Проверяет, что текст не пустой."""
    return bool(text.strip())


logging.basicConfig(
    filename="email_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(m  essage)s"
)

def log_email(recipient, status):
    """Логирование отправленных писем."""
    logging.info(f"Recipient: {recipient} | Status: {status}")


def log_email_to_db(sender_email, recipient_email, status):
    """Запись логов отправленных писем в базу данных."""
    cursor.execute(
        """
        INSERT INTO email_logs (sender_email, recipient_email, status)
        VALUES (?, ?, ?)
        """,
        (sender_email, recipient_email, status)
    )
    conn.commit()


class SendMessage(StatesGroup):
    sender_email = State()
    recipient = State()
    subject = State()
    sender_message = State()


router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Здесь ты можешь отправлять сообщения на email.",
        reply_markup=start_keyboard
    )


@router.message(F.text == "Отправить сообщения💬")
async def send_message(message: types.Message, state: FSMContext):
    await message.answer("Введите свой email.")
    await state.set_state(SendMessage.sender_email)


@router.message(SendMessage.sender_email)
async def sender(message: types.Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer("Некорректный email. Пожалуйста, введите корректный адрес.")
        return

    await state.update_data(sender_email=message.text)
    await message.answer("Введите email получателя.")
    await state.set_state(SendMessage.recipient)


@router.message(SendMessage.recipient)
async def recipient(message: types.Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer("Некорректный email. Пожалуйста, введите корректный адрес.")
        return

    await state.update_data(recipient=message.text)
    await message.answer("Введите тему сообщения.")
    await state.set_state(SendMessage.subject)


@router.message(SendMessage.subject)
async def subject(message: types.Message, state: FSMContext):
    if not is_non_empty_text(message.text):
        await message.answer("Тема сообщения не может быть пустой. Пожалуйста, введите тему.")
        return

    await state.update_data(subject=message.text)
    await message.answer("Введите ваше сообщение.")
    await state.set_state(SendMessage.sender_message)


@router.message(SendMessage.sender_message)
async def sender_message(message: types.Message, state: FSMContext):
    if not is_non_empty_text(message.text):
        await message.answer("Текст сообщения не может быть пустым. Пожалуйста, введите сообщение.")
        return

    await state.update_data(sender_message=message.text)
    data = await state.get_data()
    sender_email = data['sender_email']
    recipient = data['recipient']
    subject = data["subject"]
    sender_message = data['sender_message']

    await message.answer(
        f"Ваши данные верны?\n"
        f"Ваш email - {sender_email}\n"
        f"Email получателя - {recipient}\n"
        f"Тема сообщения - {subject}\n"
        f"Ваше сообщение - {sender_message}",
        reply_markup=sender_message_keyboard
    )


@router.callback_query(F.data == "send")
async def send(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sender_email = data['sender_email']
    recipient = data['recipient']
    subject = data["subject"]
    sender_message = data['sender_message']


    if not is_valid_email(sender_email):
        await callback.message.answer("Ваш email некорректный. Повторите попытку.")
        return

    if not is_valid_email(recipient):
        await callback.message.answer("Email получателя некорректный. Повторите попытку.")
        return

    if not is_non_empty_text(sender_message):
        await callback.message.answer("Текст сообщения не может быть пустым.")
        return

    if len(sender_message) > 1000:
        await callback.message.answer(
            f"Сообщение слишком длинное!\nДлина вашего сообщения: {len(sender_message)} символов. "
            "Максимально допустимая длина — 1000 символов.\nПожалуйста, сократите текст."
        )
        return


    sender = smtp_sender
    password = smtp_password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        msg.set_content(sender_message)

        server.send_message(msg)

        log_email_to_db(sender_email, recipient, "успешно отправлено")
        log_email(recipient, "успешно отправлено")

        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (callback.message.from_user.id, sender_email, recipient, sender_message))
        conn.commit()

        await callback.message.answer("Ваше сообщение отправлено!")

    except Exception as error:
        log_email_to_db(sender_email, recipient, f"ошибка: {error}")
        log_email(recipient, f"ошибка: {error}")
        await callback.message.answer(f"Произошла ошибка {error}!")
        print(f"{error}")

    finally:
        server.quit()