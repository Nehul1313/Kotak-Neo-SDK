import sqlite3
from datetime import datetime
import os


def get_db_path():
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("data", exist_ok=True)
    return f"data/ticks_{date_str}.db"


def get_connection():
    conn = sqlite3.connect(
        get_db_path(),
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn
