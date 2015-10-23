from datetime import datetime, timedelta, timezone

from ..core.messager import *
from ..core.data import DataConfig
from ..core.reply.Reply import Reply
from ..core.reply import ReplyCRUD

def getMentions(userId):
    return TweetAdapter.getMentions(userId, 40, DataConfig.UserDataStrategy)

def createReply(replyForm, userId):
    timeZone = timezone(timedelta(hours=int(replyForm['tzhour']), minutes=int(replyForm['tzminute'])))
    scheduledTime = datetime(datetime.now().year, int(replyForm['month']), int(replyForm['day']), int(replyForm['hour']), int(replyForm['minute']), tzinfo = timeZone)
    replyToSave = Reply(userId, replyForm['message'], scheduledTime, timeZone, replyForm['tweetId'])
    return ReplyCRUD.saveReply(replyToSave, DataConfig.ReplyDataStrategy)

def getTweet(tweetIdOrUrl, userId):
    tweet = TweetAdapter.getSingleTweet(tweetIdOrUrl, userId, DataConfig.UserDataStrategy)
    return tweet

def getScheduledReplies(userId, status):
    if status == "all":
        repliesToTransform = ReplyCRUD.getRepliesByUserId(userId, DataConfig.ReplyDataStrategy)
    else:
        repliesToTransform = ReplyCRUD.getRepliesByUserIdAndStatus(userId, status, DataConfig.ReplyDataStrategy)
    repliesToReturn = []
    for reply in repliesToTransform:
        tzInfo = str(reply.timeZone)
        if tzInfo.find('-') == -1:
            hours, minutes = tzInfo.split('+')[1].split(':')
            timeZoneDict = {"hours": int(hours), "minutes": int(minutes)}
        else:
            hours, minutes = tzInfo.split('-')[1].split(':')
            timeZoneDict = {"hours": int(hours)*-1, "minutes": int(minutes)*-1}
        repliesToReturn.append({"reply": reply, "timeZoneInformation": timeZoneDict})
    return repliesToReturn

def getSingleReply(userId, replyId):
    reply = ReplyCRUD.getReplyByReplyId(replyId, DataConfig.ReplyDataStrategy)
    if reply.userId == userId:
        tzInfo = str(reply.timeZone)
        if tzInfo.find('-') == -1:
            hours, minutes = tzInfo.split('+')[1].split(':')
            timeZoneDict = {"hours": int(hours), "minutes": int(minutes)}
        else:
            hours, minutes = tzInfo.split('-')[1].split(':')
            timeZoneDict = {"hours": int(hours)*-1, "minutes": int(minutes)*-1}
        return {"reply": reply, "timeZoneInformation": timeZoneDict}
    else:
        return {"reply": None, "reason": "You do not have permission to view this"}
