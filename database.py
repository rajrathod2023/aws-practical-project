import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/tasks.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    initialise_database()
    print("Database ready: data/tasks.db")