import sqlite3
from datetime import datetime


def create_connection(db_file="logs.db"):
    conn = sqlite3.connect(db_file, check_same_thread=False)
    return conn


def initialize_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            message TEXT
        )
    ''')
    conn.commit()


def insert_log(conn, message):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (timestamp, message) VALUES (?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
    )
    conn.commit()


def fetch_logs(conn, limit=100, offset=0):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, message FROM logs ORDER BY id DESC LIMIT ? OFFSET ?",
        (limit, offset)
    )
    return cursor.fetchall()


def count_logs(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logs")
    return cursor.fetchone()[0]
