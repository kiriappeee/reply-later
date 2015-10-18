from datetime import datetime, timedelta, timezone

from ..core.messager import *
from ..core.data import DataConfig
from ..core.reply.Reply import Reply
from ..core.reply import ReplyCRUD

def getMentions(userId):
    return TweetAdapter.getMentions(userId, 40, DataConfig.UserDataStrategy)

def createReply(replyForm, tweetId, userId):
    timeZone = timezone(timedelta(hours=int(replyForm['tzhour']), minutes=int(replyForm['tzminute'])))
    scheduledTime = datetime(datetime.now().year, int(replyForm['month']), int(replyForm['day']), int(replyForm['hour']), int(replyForm['minute']), tzinfo = timeZone)
    replyToSave = Reply(userId, replyForm['message'], scheduledTime, timeZone, tweetId)
    return ReplyCRUD.saveReply(replyToSave, DataConfig.ReplyDataStrategy)
