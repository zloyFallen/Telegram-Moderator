import sqlite3
from datetime import datetime

class User:
    """Модель для работы с пользователями."""

    def __init__(self, user_id, username, first_name, last_name, is_admin=False, is_main_admin=False, is_banned=False, last_active=None, language='ru'):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.is_main_admin = is_main_admin
        self.is_banned = is_banned
        self.last_active = last_active or datetime.now()
        self.language = language

    def save(self):
        """Сохраняет пользователя в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (id, username, first_name, last_name, is_admin, is_main_admin, is_banned, last_active, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, self.username, self.first_name, self.last_name, self.is_admin, self.is_main_admin, self.is_banned, self.last_active, self.language))
        conn.commit()
        conn.close()

    @staticmethod
    def get(user_id):
        """Возвращает пользователя по ID."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(*row)
        return None

    @staticmethod
    def is_admin(user_id):
        """Проверяет, является ли пользователь администратором."""
        user = User.get(user_id)
        return user and user.is_admin

    @staticmethod
    def is_main_admin(user_id):
        """Проверяет, является ли пользователь основным администратором."""
        user = User.get(user_id)
        return user and user.is_main_admin

    @staticmethod
    def set_language(user_id, language):
        """Устанавливает язык пользователя."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET language = ? WHERE id = ?', (language, user_id))
        conn.commit()
        conn.close()


class BannedWord:
    """Модель для работы с запрещёнными словами."""

    def __init__(self, word):
        self.word = word

    def save(self):
        """Добавляет запрещённое слово в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO banned_words (word) VALUES (?)
        ''', (self.word,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        """Возвращает все запрещённые слова."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT word FROM banned_words')
        words = [row[0] for row in cursor.fetchall()]
        conn.close()
        return words

    @staticmethod
    def delete(word):
        """Удаляет запрещённое слово из базы данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM banned_words WHERE word = ?', (word,))
        conn.commit()
        conn.close()


class ChatSettings:
    """Модель для работы с настройками чата."""

    def __init__(self, chat_id, welcome_enabled=False, welcome_media=None):
        self.chat_id = chat_id
        self.welcome_enabled = welcome_enabled
        self.welcome_media = welcome_media

    def save(self):
        """Сохраняет настройки чата в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO chat_settings (chat_id, welcome_enabled, welcome_media)
            VALUES (?, ?, ?)
        ''', (self.chat_id, self.welcome_enabled, self.welcome_media))
        conn.commit()
        conn.close()

    @staticmethod
    def get(chat_id):
        """Возвращает настройки чата по ID."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM chat_settings WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ChatSettings(*row)
        return None


class ProSubscription:
    """Модель для работы с подписками на PRO версию."""

    def __init__(self, chat_id, is_pro=False, payment_id=None):
        self.chat_id = chat_id
        self.is_pro = is_pro
        self.payment_id = payment_id

    def save(self):
        """Сохраняет информацию о подписке в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO pro_subscriptions (chat_id, is_pro, payment_id)
            VALUES (?, ?, ?)
        ''', (self.chat_id, self.is_pro, self.payment_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get(chat_id):
        """Возвращает информацию о подписке для чата."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pro_subscriptions WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ProSubscription(*row)
        return None


class ConnectedChat:
    """Модель для работы с подключёнными чатами."""

    def __init__(self, chat_id, chat_title):
        self.chat_id = chat_id
        self.chat_title = chat_title

    def save(self):
        """Сохраняет информацию о чате в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO connected_chats (chat_id, chat_title)
            VALUES (?, ?)
        ''', (self.chat_id, self.chat_title))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        """Возвращает список всех подключённых чатов."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM connected_chats')
        rows = cursor.fetchall()
        conn.close()
        return rows


class AntiBotSettings:
    """Модель для работы с настройками анти-бот системы."""

    def __init__(self, chat_id, enabled=False, captcha_type='digits', kick_time=60):
        self.chat_id = chat_id
        self.enabled = enabled
        self.captcha_type = captcha_type
        self.kick_time = kick_time

    def save(self):
        """Сохраняет настройки анти-бот системы в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO anti_bot_settings (chat_id, enabled, captcha_type, kick_time)
            VALUES (?, ?, ?, ?)
        ''', (self.chat_id, self.enabled, self.captcha_type, self.kick_time))
        conn.commit()
        conn.close()

    @staticmethod
    def get(chat_id):
        """Возвращает настройки анти-бот системы для чата."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM anti_bot_settings WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return AntiBotSettings(*row)
        return None


class LogChannel:
    """Модель для работы с каналом логов."""

    def __init__(self, chat_id, log_channel_id=None):
        self.chat_id = chat_id
        self.log_channel_id = log_channel_id

    def save(self):
        """Сохраняет ID канала логов в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO log_channel (chat_id, log_channel_id)
            VALUES (?, ?)
        ''', (self.chat_id, self.log_channel_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get(chat_id):
        """Возвращает ID канала логов для чата."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM log_channel WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return LogChannel(*row)
        return None


class AutoDeleteSettings:
    """Модель для работы с настройками автоматического удаления сообщений."""

    def __init__(self, chat_id, enabled=False, delete_time=60):
        self.chat_id = chat_id
        self.enabled = enabled
        self.delete_time = delete_time

    def save(self):
        """Сохраняет настройки автоматического удаления в базу данных."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO auto_delete_settings (chat_id, enabled, delete_time)
            VALUES (?, ?, ?)
        ''', (self.chat_id, self.enabled, self.delete_time))
        conn.commit()
        conn.close()

    @staticmethod
    def get(chat_id):
        """Возвращает настройки автоматического удаления для чата."""
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM auto_delete_settings WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return AutoDeleteSettings(*row)
        return None