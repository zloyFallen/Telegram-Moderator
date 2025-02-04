import logging
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import User, ChatSettings, BannedWord, ProSubscription, ConnectedChat, AntiBotSettings, LogChannel, AutoDeleteSettings

# Логирование
logger = logging.getLogger(__name__)

# Главное меню админки
async def admin_panel(message: types.Message):
    if not User.is_admin(message.from_user.id):
        logger.warning(f"Пользователь {message.from_user.id} попытался получить доступ к админке без прав.")
        await message.answer("❌ У вас нет прав администратора.")
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Приветствия", callback_data="welcome_settings"),
        InlineKeyboardButton("Запрещённые слова", callback_data="banned_words"),
        InlineKeyboardButton("Выдать права админа", callback_data="grant_admin"),
        InlineKeyboardButton("Удалить неактивных", callback_data="clean_inactive"),
        InlineKeyboardButton("Статистика", callback_data="show_stats"),
        InlineKeyboardButton("Просмотр чатов", callback_data="show_connected_chats"),
        InlineKeyboardButton("Анти-бот система", callback_data="anti_bot_settings"),
        InlineKeyboardButton("Канал логов", callback_data="log_channel_settings"),
        InlineKeyboardButton("Автоудаление", callback_data="auto_delete_settings")
    )

    await message.answer("Админ-панель:", reply_markup=keyboard)
    logger.info(f"Админ-панель открыта пользователем {message.from_user.id}.")

# Обработка нажатий на кнопки
async def handle_admin_callback(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    user_id = callback.from_user.id

    if not User.is_admin(user_id):
        await callback.answer("❌ У вас нет прав администратора.")
        return

    if callback.data == "welcome_settings":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Включить приветствия", callback_data="welcome_on"),
            InlineKeyboardButton("Выключить приветствия", callback_data="welcome_off"),
            InlineKeyboardButton("Установить медиа", callback_data="welcome_set_media"),
            InlineKeyboardButton("Назад", callback_data="admin_panel")
        )
        await callback.message.edit_text("Настройки приветствий:", reply_markup=keyboard)

    elif callback.data == "welcome_on":
        settings = ChatSettings.get(chat_id)
        if not settings:
            settings = ChatSettings(chat_id)
        settings.welcome_enabled = True
        settings.save()
        await callback.message.edit_text("✅ Приветствия включены.")

    elif callback.data == "welcome_off":
        settings = ChatSettings.get(chat_id)
        if not settings:
            settings = ChatSettings(chat_id)
        settings.welcome_enabled = False
        settings.save()
        await callback.message.edit_text("❌ Приветствия выключены.")

    elif callback.data == "welcome_set_media":
        await callback.message.edit_text("Ответьте на сообщение с фото или гифкой, чтобы установить медиа для приветствия.")

    elif callback.data == "banned_words":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Добавить слово", callback_data="add_banned_word"),
            InlineKeyboardButton("Удалить слово", callback_data="remove_banned_word"),
            InlineKeyboardButton("Назад", callback_data="admin_panel")
        )
        await callback.message.edit_text("Управление запрещёнными словами:", reply_markup=keyboard)

    elif callback.data == "grant_admin":
        await callback.message.edit_text("Ответьте на сообщение пользователя, чтобы выдать ему права администратора.")

    elif callback.data == "clean_inactive":
        await callback.message.edit_text("Функция удаления неактивных аккаунтов в разработке.")

    elif callback.data == "show_stats":
        await show_stats(callback)

    elif callback.data == "show_connected_chats":
        await show_connected_chats(callback)

    elif callback.data == "anti_bot_settings":
        await anti_bot_settings(callback.message)

    elif callback.data == "log_channel_settings":
        await log_channel_settings(callback.message)

    elif callback.data == "auto_delete_settings":
        await auto_delete_settings(callback.message)

    elif callback.data == "admin_panel":
        await admin_panel(callback.message)

    await callback.answer()

# Управление анти-бот системой
async def anti_bot_settings(message: types.Message):
    chat_id = message.chat.id
    settings = AntiBotSettings.get(chat_id)
    if not settings:
        settings = AntiBotSettings(chat_id)

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Включить", callback_data="anti_bot_enable"),
        InlineKeyboardButton("Выключить", callback_data="anti_bot_disable"),
        InlineKeyboardButton("Изменить тип капчи", callback_data="anti_bot_change_type"),
        InlineKeyboardButton("Изменить время", callback_data="anti_bot_change_time"),
        InlineKeyboardButton("Назад", callback_data="admin_panel")
    )

    status = "включена" if settings.enabled else "выключена"
    await message.answer(f"Настройки анти-бот системы (статус: {status}):", reply_markup=keyboard)

# Управление каналом логов
async def log_channel_settings(message: types.Message):
    chat_id = message.chat.id
    log_channel = LogChannel.get(chat_id)
    if not log_channel:
        log_channel = LogChannel(chat_id)

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Установить канал", callback_data="set_log_channel"),
        InlineKeyboardButton("Удалить канал", callback_data="remove_log_channel"),
        InlineKeyboardButton("Назад", callback_data="admin_panel")
    )

    await message.answer("Настройки канала логов:", reply_markup=keyboard)

# Управление автоматическим удалением сообщений
async def auto_delete_settings(message: types.Message):
    chat_id = message.chat.id
    settings = AutoDeleteSettings.get(chat_id)
    if not settings:
        settings = AutoDeleteSettings(chat_id)

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Включить", callback_data="auto_delete_enable"),
        InlineKeyboardButton("Выключить", callback_data="auto_delete_disable"),
        InlineKeyboardButton("Изменить время", callback_data="auto_delete_change_time"),
        InlineKeyboardButton("Назад", callback_data="admin_panel")
    )

    status = "включено" if settings.enabled else "выключено"
    await message.answer(f"Настройки автоматического удаления (статус: {status}):", reply_markup=keyboard)

# Регистрация обработчиков
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=["admin"])
    dp.register_callback_query_handler(handle_admin_callback)