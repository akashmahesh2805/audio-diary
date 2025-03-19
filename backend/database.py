"""
database.py - Stores and retrieves diary entries

- Uses SQLite to store:
  - Transcriptions
  - Detected emotions
  - AI-generated responses
- Retrieves previous diary entries.
"""

import sqlite3

DB_FILE = "diary.db"

def init_db():
    """
    Initializes the SQLite database.
    - Creates a table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS diary_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text TEXT,
                        emotion TEXT,
                        response TEXT
                      )''')
    conn.commit()
    conn.close()

def store_entry(text, emotion, response):
    """
    Stores a diary entry in the database.
    - Saves text, emotion, and response for tracking.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO diary_entries (text, emotion, response) VALUES (?, ?, ?)", (text, emotion, response))
    conn.commit()
    conn.close()

def get_entries():
    """
    Fetches all diary entries.
    - Returns structured data with text, emotion, and response.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT text, emotion, response FROM diary_entries ORDER BY id DESC")
    entries = cursor.fetchall()
    conn.close()
    return [{"text": t, "emotion": e, "response": r} for t, e, r in entries]

# Ensure the database is initialized on startup
init_db()
