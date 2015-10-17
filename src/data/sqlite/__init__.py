import sqlite3
import os

if not os.path.exists('src/data/sqlite/data.db'):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE user(
    username VARCHAR(200) UNIQUE,
    authToken TEXT,
    secretToken TEXT,
    timezoneDifferenceSeconds INT,
    timeZoneDifferenceDays INT
    )""")
    conn.commit()
    conn.close()
