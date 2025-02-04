from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.models import BannedWord, LogChannel
from datetime import datetime

# Фильтр запрещённых слов
async def check_banned_words(message: types.Message):
    banned_words = BannedWord.get_all()
    for word in banned_words:
        if word in message.text.lower():
            await message.delete()
            await message.answer(f"@{message.from_user.username}, ваше сообщение удалено из-за запрещённого слова.")

            # Отправляем лог в канал
            log_channel = LogChannel.get(message.chat.id)
            if log_channel and log_channel.log_channel_id:
                log_text = (
                    f"🚨 Блокировка пользователя\n"
                    f"ID: {message.from_user.id}\n"
                    f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"Причина: Использование запрещённого слова ({word})"
                )
                await bot.send_message(log_channel.log_channel_id, log_text)

            break

# Регистрация обработчиков
def register_handlers_moderation(dp: Dispatcher):
    dp.register_message_handler(check_banned_words)