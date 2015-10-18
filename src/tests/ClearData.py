import sqlite3

def clearData():
    conn = sqlite3.connect('src/data/sqlite/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM user")
    cur.execute("DELETE FROM reply")
    conn.commit()
    conn.close()

