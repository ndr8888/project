import sqlite3

conn = sqlite3.connect(r'db_data\questions.db')
cur = conn.cursor()
result = cur.execute("DELETE FROM questions WHERE id = 16").fetchall()
conn.commit()
conn.close()