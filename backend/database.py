import sqlite3

DB_FILE = "diary.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY,
            text TEXT,
            emotion TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

    

def store_entry(text, emotion, response):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diary (text, emotion, response) VALUES (?, ?, ?)", (text, emotion["emotion"], response))
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diary")
    entries = cursor.fetchall()
    conn.close()
    return entries

init_db()
