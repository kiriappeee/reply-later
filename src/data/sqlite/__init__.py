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
    cur.execute("""CREATE TABLE reply(
    userId INT,
    message TEXT,
    scheduledTime DATETIME,
    timeZoneDifferenceSeconds INT,
    timeZoneDifferenceDays INT,
    tweetId VARCHAR(100),
    sentStatus VARCHAR(20),
    FOREIGN KEY(userId) REFERENCES user (ROWID)
            )""")
    conn.commit()
    conn.close()
