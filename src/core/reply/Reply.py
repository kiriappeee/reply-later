class Reply:
    def __init__(self, userId, message, scheduledTime, timeZone, tweetId, replyId=None):
        self.userId = userId
        self.message = message
        self.scheduledTime = scheduledTime
        self.timeZone = timeZone
        self.tweetId = tweetId
        self.replyId = replyId
