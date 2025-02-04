import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            is_admin BOOLEAN DEFAULT 0,
            is_main_admin BOOLEAN DEFAULT 0,
            is_banned BOOLEAN DEFAULT 0,
            last_active TIMESTAMP,
            language TEXT DEFAULT 'ru'
        )
    ''')

    # Таблица запрещённых слов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banned_words (
            word TEXT PRIMARY KEY
        )
    ''')

    # Таблица настроек чата
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_settings (
            chat_id INTEGER PRIMARY KEY,
            welcome_enabled BOOLEAN DEFAULT 0,
            welcome_media TEXT
        )
    ''')

    # Таблица подписок на PRO версию
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pro_subscriptions (
            chat_id INTEGER PRIMARY KEY,
            is_pro BOOLEAN DEFAULT 0,
            payment_id TEXT
        )
    ''')

    # Таблица подключённых чатов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connected_chats (
            chat_id INTEGER PRIMARY KEY,
            chat_title TEXT
        )
    ''')

    # Таблица настроек анти-бот системы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anti_bot_settings (
            chat_id INTEGER PRIMARY KEY,
            enabled BOOLEAN DEFAULT 0,
            captcha_type TEXT DEFAULT 'digits',
            kick_time INTEGER DEFAULT 60
        )
    ''')

    # Таблица для хранения ID канала логов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log_channel (
            chat_id INTEGER PRIMARY KEY,
            log_channel_id TEXT
        )
    ''')

    # Таблица для хранения настроек автоматического удаления сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auto_delete_settings (
            chat_id INTEGER PRIMARY KEY,
            enabled BOOLEAN DEFAULT 0,
            delete_time INTEGER DEFAULT 60
        )
    ''')

    conn.commit()
    conn.close()