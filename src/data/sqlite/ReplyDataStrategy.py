import sqlite3
from datetime import datetime, timezone, timedelta
import time
from ...core.reply.Reply import Reply

def saveReply(replyToSave):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    cur = conn.cursor()
    timeZoneInformation = replyToSave.timeZone.utcoffset(datetime.now())
    cur.execute("""INSERT INTO reply (
    userId,
    message,
    scheduledTime,
    timeZoneDifferenceSeconds,
    timeZoneDifferenceDays,
    tweetId,
    sentStatus
    ) VALUES (?, ?, ?, ?, ?, ?, ?)""",(
        replyToSave.userId,
        replyToSave.message,
        replyToSave.scheduledTime,
        timeZoneInformation.seconds,
        timeZoneInformation.days,
        replyToSave.tweetId,
        replyToSave.sentStatus
        ))
    lastRowId = cur.lastrowid
    conn.commit()
    conn.close()
    return lastRowId

def getReplyByReplyId(replyId):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT ROWID, * FROM reply WHERE ROWID=:replyid", {"replyid": replyId})
    result = cur.fetchone()
    conn.close()
    if result:
        return convertReplyRowToObject(result)

def updateReply(replyToUpdate):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    cur = conn.cursor()
    timeZoneInformation = replyToUpdate.timeZone.utcoffset(datetime.now())
    cur.execute("UPDATE reply SET message=:value WHERE ROWID=:replyid",{"value": replyToUpdate.message, "replyid": replyToUpdate.replyId})
    cur.execute("UPDATE reply SET scheduledTime=:value WHERE ROWID=:replyid",{"value": replyToUpdate.scheduledTime, "replyid": replyToUpdate.replyId})
    cur.execute("UPDATE reply SET timeZoneDifferenceSeconds=:value WHERE ROWID=:replyid",{"value": timeZoneInformation.seconds, "replyid": replyToUpdate.replyId})
    cur.execute("UPDATE reply SET timeZoneDifferenceDays=:value WHERE ROWID=:replyid",{"value": timeZoneInformation.days, "replyid": replyToUpdate.replyId})
    cur.execute("UPDATE reply SET sentStatus=:value WHERE ROWID=:replyid",{"value": replyToUpdate.sentStatus, "replyid": replyToUpdate.replyId})
    conn.commit()
    conn.close()
    return True

def cancelReply(replyToCancel):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    cur = conn.cursor()
    cur.execute("UPDATE reply SET sentStatus=:value WHERE ROWID=:replyid",{"value": replyToCancel.sentStatus, "replyid": replyToCancel.replyId})
    conn.commit()
    conn.close()
    return True

def getRepliesByUserId(userId):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT ROWID, * FROM reply WHERE userId=:userid",{"userid": userId})
    results = cur.fetchall()
    repliesToReturn = []
    for result in results:
        repliesToReturn.append(convertReplyRowToObject(result))
    return repliesToReturn

def getRepliesByUserIdAndStatus(userId, status):
    conn = sqlite3.connect('src/data/sqlite/data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT ROWID, * FROM reply WHERE userId=:userid AND sentStatus=:status",{"userid": userId, "status": status})
    results = cur.fetchall()
    repliesToReturn = []
    for result in results:
        repliesToReturn.append(convertReplyRowToObject(result))
    return repliesToReturn

def convertReplyRowToObject(result):
    timeZoneInformation = [result['timeZoneDifferenceDays'], result['timeZoneDifferenceSeconds']]
    if timeZoneInformation[0] == -1:
        tz = timezone(timedelta(seconds=result['timeZoneDifferenceSeconds'] * -1))
    else:
        tz = timezone(timedelta(seconds=result['timeZoneDifferenceSeconds']))

    t = time.strptime(result['scheduledTime'].split('+')[0].split('.')[0], "%Y-%m-%d %H:%M:%S")
    if len(result['scheduledTime'].split('+')[0].split('.')) == 1:
        microsecond = 0
    else:
        microsecond = int(result['scheduledTime'].split('+')[0].split('.')[1])

    d = datetime(t.tm_year, t.tm_mon, t.tm_mday, hour=t.tm_hour, minute = t.tm_min, second = t.tm_sec, microsecond=microsecond, tzinfo=tz)
    replyToReturn = Reply(result['userId'],
            result['message'],
            d,
            tz,
            result['tweetId'],
            result['sentStatus'],
            replyId = result['ROWID'])
    return replyToReturn
