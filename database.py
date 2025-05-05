import sqlite3

DB_NAME = "common.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            first_name TEXT,
            username TEXT,
            email TEXT DEFAULT NULL,
            phone TEXT DEFAULT NULL,
            is_subscription INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_or_update_user(telegram_id, first_name, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (telegram_id, first_name, username)
        VALUES (?, ?, ?)
    ''', (telegram_id, first_name, username))
    conn.commit()
    conn.close()

def update_user_email(telegram_id, email):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET email = ? WHERE telegram_id = ?', (email, telegram_id))
    conn.commit()
    conn.close()

def update_user_phone(telegram_id, phone):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET phone = ? WHERE telegram_id = ?', (phone, telegram_id))
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_user_subscription(telegram_id, is_active=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE users SET is_subscription = ? WHERE telegram_id = ?',
        (1 if is_active else 0, telegram_id)
    )
    conn.commit()
    conn.close()
