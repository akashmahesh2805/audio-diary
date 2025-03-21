import sqlite3

# Initialize DB
conn = sqlite3.connect("diary.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    emotion TEXT,
    response TEXT
)
""")
conn.commit()

def store_entry(text, emotion, response):
    """Stores a conversation entry in the database."""
    cursor.execute("INSERT INTO diary (text, emotion, response) VALUES (?, ?, ?)", (text, emotion, response))
    conn.commit()

def get_entries():
    """Retrieves all stored entries from the database."""
    cursor.execute("SELECT * FROM diary")
    return cursor.fetchall()
