import sqlite3

conn = sqlite3.connect("diary.db", check_same_thread=False)
cursor = conn.cursor()

# Insert a test entry
cursor.execute("INSERT INTO diary (text, emotion, response) VALUES (?, ?, ?)", 
               ("I had a great day", "Happy", "Glad you did!"))

conn.commit()
conn.close()

print("Test entry added to database.")
