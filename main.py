import logging
from aiogram import Bot, Dispatcher, executor
from database.db import init_db
from handlers.admin import register_handlers_admin
from handlers.user import register_handlers_user
from handlers.moderation import register_handlers_moderation

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат логов
    handlers=[
        logging.FileHandler("bot.log"),  # Логи записываются в файл bot.log
        logging.StreamHandler()  # Логи выводятся в терминал (можно удалить, если не нужно)
    ]
)

logger = logging.getLogger(__name__)

# Настройки
TELEGRAM_BOT_TOKEN = '8037281434:AAHQUVlXH5koGSSmTxKu5tfPm0Gr4zFJp0k'

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация базы данных
init_db()

# Регистрация обработчиков
register_handlers_admin(dp)
register_handlers_user(dp)
register_handlers_moderation(dp)

# Запуск бота
if __name__ == '__main__':
    logger.info("Бот запущен")  # Логируем запуск бота
    executor.start_polling(dp, skip_updates=True)