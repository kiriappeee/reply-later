from . import TweetAdapter
from . import MessageBreaker
from ..reply import ReplyCRUD
from ..data import DataConfig

def sendMessage(replyId, dataStrategyInitializer):
    DataConfig.initializeDataStrategy(dataStrategyInitializer)
    reply = ReplyCRUD.getReplyByReplyId(replyId, DataConfig.ReplyDataStrategy)
    messagesToSend = MessageBreaker.breakMessage(reply.message, reply.tweetId)
    replyIdList = []
    for message in messagesToSend:
        replyId = TweetAdapter.sendReply(message, replyId)
        replyIdList.append(replyId)
    reply.sentStatus = "sent"
    ReplyCRUD.saveReply(reply, DataConfig.ReplyDataStrategy)
    return {"result": "success", "value":{"tweets": replyIdList} }

