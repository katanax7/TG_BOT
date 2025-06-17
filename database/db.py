import sqlite3
from database import models

DB_PATH = "bot.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    models.create_tables(conn)
    conn.close()

def add_user(telegram_id: int, name: str, role: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users (telegram_id, name, role) VALUES (?, ?, ?)",
        (telegram_id, name, role)
    )
    conn.commit()
    conn.close()
