from datetime import datetime, timezone, timedelta
import sqlite3

from ...core.user.User import User

def saveUser(userToSave):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    cur = conn.cursor()
    timeZoneInformation = userToSave.timeZone.utcoffset(datetime.now())
    cur.execute("""INSERT INTO user (username,
            authToken,
            secretToken,
            timezoneDifferenceSeconds,
            timeZoneDifferenceDays
            ) VALUES (?,?,?,?,?)""", (userToSave.username,
                userToSave.authToken,
                userToSave.secretToken,
                timeZoneInformation.seconds,
                timeZoneInformation.days
                ))
    lastRowId = cur.lastrowid
    conn.commit()
    conn.close()
    return lastRowId

def updateUser(userToUpdate):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    cur = conn.cursor()
    timeZoneInformation = userToUpdate.timeZone.utcoffset(datetime.now())
    cur.execute("UPDATE user SET username=:value WHERE ROWID=:userid",{"value": userToUpdate.username, "userid": userToUpdate.userId})
    cur.execute("UPDATE user SET authToken=:value WHERE ROWID=:userid",{"value": userToUpdate.authToken, "userid": userToUpdate.userId})
    cur.execute("UPDATE user SET secretToken=:value WHERE ROWID=:userid",{"value": userToUpdate.secretToken, "userid": userToUpdate.userId})
    cur.execute("UPDATE user SET timezoneDifferenceSeconds=:value WHERE ROWID=:userid",{"value": timeZoneInformation.seconds, "userid": userToUpdate.userId})
    cur.execute("UPDATE user SET timeZoneDifferenceDays=:value WHERE ROWID=:userid",{"value": timeZoneInformation.days, "userid": userToUpdate.userId})
    conn.commit()
    conn.close()
    return True

def getUserById(userId):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT ROWID, * FROM user WHERE ROWID=:userid", {"userid": userId})
    result = cur.fetchone()
    conn.close()
    if result:
        userToReturn = convertRowToUser(result)
        return userToReturn

def getUserByUsername(username):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT ROWID, * FROM user WHERE username=:username", {"username": username})
    result = cur.fetchone()
    conn.close()
    if result:
        userToReturn = convertRowToUser(result)
        return userToReturn

def convertRowToUser(row):
    timeZoneInformation = [row['timeZoneDifferenceDays'], row['timeZoneDifferenceSeconds']]
    if timeZoneInformation[0] == -1:
        tz = timezone(timedelta(seconds=row['timeZoneDifferenceSeconds'] * -1))
    else:
        tz = timezone(timedelta(seconds=row['timeZoneDifferenceSeconds']))
    userToReturn = User(row['username'],
            row['authToken'],
            row['secretToken'],
            tz,
            userId = row['ROWID'])
    return userToReturn
