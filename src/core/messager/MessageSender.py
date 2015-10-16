from . import TweetAdapter
from . import MessageBreaker
from ..reply import ReplyCRUD
from ..data import DataConfig

def sendMessage(replyId, dataStrategyInitializer):
    DataConfig.initializeDataStrategy(dataStrategyInitializer)
    reply = ReplyCRUD.getReplyByReplyId(replyId, DataConfig.ReplyDataStrategy)
    messagesToSend = MessageBreaker.breakMessage(reply.message, reply.tweetId, reply.userId, DataConfig.UserDataStrategy)
    tweetIdList = []
    tweetId = reply.tweetId
    for message in messagesToSend:
        tweetId = TweetAdapter.sendReply(message, tweetId, reply.userId, DataConfig.UserDataStrategy)
        tweetIdList.append(tweetId)
    reply.sentStatus = "sent"
    ReplyCRUD.updateReply(reply, DataConfig.ReplyDataStrategy)
    return {"result": "success", "value":{"tweets": tweetIdList} }

