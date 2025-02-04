from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import User, ChatSettings, AntiBotSettings, LogChannel, AutoDeleteSettings
import random
import asyncio

# Приветствие и выбор языка
async def start(message: types.Message):
    user = User.get(message.from_user.id)
    if not user:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("🇷🇺 Русский", callback_data="set_language_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="set_language_en")
        )
        await message.answer("Выберите язык / Choose language:", reply_markup=keyboard)
    else:
        if user.language == 'ru':
            await message.answer("Привет! Чем могу помочь?")
        else:
            await message.answer("Hello! How can I help you?")

# Обработка выбора языка
async def set_language(callback: types.CallbackQuery):
    language = callback.data.split("_")[-1]
    User.set_language(callback.from_user.id, language)

    if language == 'ru':
        await callback.message.edit_text("✅ Язык установлен: Русский")
    else:
        await callback.message.edit_text("✅ Language set: English")

    await callback.answer()

# Приветствие нового пользователя
async def welcome_new_user(message: types.Message):
    chat_id = message.chat.id
    settings = ChatSettings.get(chat_id)
    if not settings or not settings.welcome_enabled:
        return

    new_user = message.new_chat_members[0]
    user = User.get(new_user.id)
    language = user.language if user else 'ru'

    if language == 'ru':
        welcome_text = f"Добро пожаловать, {new_user.first_name}!"
    else:
        welcome_text = f"Welcome, {new_user.first_name}!"

    if settings.welcome_media:
        if settings.welcome_media.startswith("Ag"):
            sent_message = await message.answer_animation(settings.welcome_media, caption=welcome_text)
        else:
            sent_message = await message.answer_photo(settings.welcome_media, caption=welcome_text)
    else:
        sent_message = await message.answer(welcome_text)

    # Удаляем сообщение через заданное время
    await delete_message_after_delay(sent_message)

# Проверка новых участников
async def check_new_member(message: types.Message):
    chat_id = message.chat.id
    settings = AntiBotSettings.get(chat_id)
    if not settings or not settings.enabled:
        return

    captcha = generate_captcha(settings.captcha_type)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Я не бот", callback_data=f"captcha_{captcha}"))
    sent_message = await message.answer(f"Докажите, что вы не бот. Введите код: {captcha}", reply_markup=keyboard)

    # Удаляем сообщение через заданное время
    await delete_message_after_delay(sent_message)

    # Удаление пользователя, если он не решил капчу
    await asyncio.sleep(settings.kick_time)
    try:
        await message.chat.kick(user_id=message.from_user.id)
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")

# Обработка решения капчи
async def handle_captcha(callback: types.CallbackQuery):
    await callback.answer("✅ Вы успешно прошли проверку!")
    await callback.message.delete()

# Генерация капчи
def generate_captcha(captcha_type='digits'):
    if captcha_type == 'digits':
        return ''.join(random.choices('0123456789', k=4))
    elif captcha_type == 'letters':
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
    else:
        return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))

# Удаление сообщений через заданное время
async def delete_message_after_delay(message: types.Message):
    chat_id = message.chat.id
    settings = AutoDeleteSettings.get(chat_id)
    if not settings or not settings.enabled:
        return

    await asyncio.sleep(settings.delete_time)
    try:
        await message.delete()
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")

# Регистрация обработчиков
def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
    dp.register_callback_query_handler(set_language, lambda c: c.data.startswith("set_language_"))
    dp.register_message_handler(welcome_new_user, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(check_new_member, content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_callback_query_handler(handle_captcha, lambda c: c.data.startswith("captcha_"))