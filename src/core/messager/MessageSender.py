from . import TweetAdapter
from . import MessageBreaker
from ..scheduler import Scheduler
from ..reply import ReplyCRUD
from ..data import DataConfig
import argparse

def sendMessage(replyId, dataStrategyInitializer):
    DataConfig.initializeDataStrategy(dataStrategyInitializer)
    reply = ReplyCRUD.getReplyByReplyId(replyId, DataConfig.ReplyDataStrategy)
    print(reply.sentStatus)
    print(DataConfig.ReplyDataStrategy)
    messagesToSend = MessageBreaker.breakMessage(reply.message, reply.tweetId, reply.userId, DataConfig.UserDataStrategy)
    tweetIdList = []
    tweetId = reply.tweetId
    for message in messagesToSend:
        tweetId = TweetAdapter.sendReply(message, tweetId, reply.userId, DataConfig.UserDataStrategy)
        tweetIdList.append(tweetId)
    reply.sentStatus = "sent"
    print(reply.sentStatus)
    print(ReplyCRUD.updateReply(reply, DataConfig.ReplyDataStrategy))
    return {"result": "success", "value":{"tweets": tweetIdList} }


if __name__ == "__main__":
    f = open('executed', 'w')
    parser = argparse.ArgumentParser()
    parser.add_argument('--data')
    parser.add_argument('--id')
    args = parser.parse_args()
    f.write(args.id + ' ' + args.data)
    f.close()
    sendMessage(args.id, args.data)

