import sqlite3


conn = sqlite3.connect("Users.db")
cursor = conn.cursor()


cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone INTEGER NOT NULL,
            chat_id INTEGER,
            time_schedule TEXT
        )
    """)
conn.commit()