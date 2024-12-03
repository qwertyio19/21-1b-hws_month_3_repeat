import sqlite3

conn = sqlite3.connect("Users.db")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        sender TEXT NOT NULL,
        recipient TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS email_logs (
    id SERIAL PRIMARY KEY,
    sender_email VARCHAR(255),
    recipient_email VARCHAR(255),
    status TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()