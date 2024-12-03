import re
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ContentType
from app.keyboards import start_keyboards, confirm_keyboards
from config import smtp_sender, smtp_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import aiosmtplib

router = Router()

class SendState(StatesGroup):
    recipient_email = State()
    subject = State()
    content = State()

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Я помогу отправить сообщения, фото, видео и аудио на email!",
        reply_markup=start_keyboards
    )

@router.callback_query(F.data.in_({"message", "photo", "video", "audio"}))
async def start_sending(callback: types.CallbackQuery, state: FSMContext):
    content_type = callback.data
    await state.update_data(content_type=content_type)
    await callback.message.answer("Введите email получателя:")
    await state.set_state(SendState.recipient_email)

@router.message(SendState.recipient_email)
async def recipient_email_handler(message: types.Message, state: FSMContext):
    email = message.text.strip()
    if "@" not in email or "." not in email:
        await message.answer("Пожалуйста, введите корректный email!")
        return
    await state.update_data(recipient_email=email)
    await message.answer("Введите тему сообщения:")
    await state.set_state(SendState.subject)


@router.message(SendState.subject)
async def subject_handler(message: types.Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)
    data = await state.get_data()
    content_type = data['content_type']
    if content_type == "message":
        await message.answer("Введите текст сообщения:")
    else:
        await message.answer(f"Прикрепите {content_type} или отправьте ссылку:")
    await state.set_state(SendState.content)

@router.message(SendState.content, F.content_type.in_([ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.AUDIO]))
async def content_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    content_type = data['content_type']

    if content_type == "message":
        await state.update_data(content=message.text)
    elif content_type == "photo":
        await state.update_data(content=message.photo[-1].file_id)
    elif content_type == "video":
        await state.update_data(content=message.video.file_id)
    elif content_type == "audio":
        await state.update_data(content=message.audio.file_id)

    recipient_email = data['recipient_email']
    subject = data['subject']
    await message.answer(
        f"Отправить {content_type} на email {recipient_email} с темой \"{subject}\"?",
        reply_markup=confirm_keyboards[content_type]
    )

@router.callback_query(F.data.in_({"confirm_message", "confirm_photo", "confirm_video", "confirm_audio", 
                                   "cancel_message", "cancel_photo", "cancel_video", "cancel_audio"}))
async def confirm_or_cancel(callback: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        

        recipient_email = data.get('recipient_email')
        subject = data.get('subject')
        content_type = data.get('content_type')
        content = data.get('content')

        if not recipient_email or not subject or not content_type or not content:
            await callback.message.answer("Ошибка: данные для отправки неполные. Попробуйте снова.")
            await state.clear()
            return

        sender = smtp_sender
        password = smtp_password

        bot = callback.bot
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient_email

        if content_type == "message":
            msg.attach(MIMEText(content, "plain"))
        else:
            file_info = await bot.get_file(content)
            file = await bot.download_file(file_info.file_path)
            attachment = None

            if content_type == "photo":
                attachment = MIMEBase('image', 'jpeg')
                filename = "photo.jpg"
            elif content_type == "video":
                attachment = MIMEBase('video', 'mp4')
                filename = "video.mp4"
            elif content_type == "audio":
                attachment = MIMEBase('audio', 'mpeg')
                filename = "audio.mp3"

            if attachment:
                attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(attachment)


        smtp_client = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587, start_tls=True)
        await smtp_client.connect()
        await smtp_client.login(sender, password)
        await smtp_client.send_message(msg)
        await smtp_client.quit()

        await callback.message.answer("Сообщение успешно отправлено! ✅")
    except Exception as e:
        await callback.message.answer(f"Ошибка при отправке: {e}")
    finally:
        await state.clear()