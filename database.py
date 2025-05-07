import psycopg2
from psycopg2.extras import RealDictCursor
import config

conn = psycopg2.connect(
    host=config.PG_HOST,
    port=config.PG_PORT,
    user=config.PG_USER,
    password=config.PG_PASSWORD,
    database=config.PG_DB
)

conn.autocommit = True
cursor = conn.cursor(cursor_factory=RealDictCursor)

def init_db():
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS common_schema;
        CREATE TABLE IF NOT EXISTS common_schema.users (
            telegram_id BIGINT PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            email TEXT,
            phone TEXT,
            is_subscription BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)

def add_or_update_user(telegram_id, first_name, username):
    cursor.execute("""
        INSERT INTO common_schema.users (telegram_id, first_name, username)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id)
        DO UPDATE SET first_name = EXCLUDED.first_name, username = EXCLUDED.username;
    """, (telegram_id, first_name, username))

def update_user_email(telegram_id, email):
    cursor.execute("UPDATE common_schema.users SET email=%s WHERE telegram_id=%s", (email, telegram_id))

def update_user_phone(telegram_id, phone):
    cursor.execute("UPDATE common_schema.users SET phone=%s WHERE telegram_id=%s", (phone, telegram_id))

def update_user_subscription(telegram_id, status):
    cursor.execute("UPDATE common_schema.users SET is_subscription=%s WHERE telegram_id=%s", (status, telegram_id))

def get_user(telegram_id):
    cursor.execute("SELECT * FROM common_schema.users WHERE telegram_id=%s", (telegram_id,))
    return cursor.fetchone()
