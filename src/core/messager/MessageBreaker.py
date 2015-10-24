from . import TweetAdapter
def breakMessage(messageToBreak, tweetId, userId, userDataStrategy):
    if len(messageToBreak) <= 140:
        return [ messageToBreak ]
    username = TweetAdapter.getUsernameForTweet(tweetId, userId, userDataStrategy)
    messagesToSend = []
    while messageToBreak!="":
        if len(messageToBreak) > 140:
            if messageToBreak[140] != " ":
                cutOffIndex = messageToBreak[0:140].rfind(" ") + 1
            else:
                cutOffIndex = 140
            messagesToSend.append(messageToBreak[:cutOffIndex].rstrip())
            
            messageToBreak = "@%s %s"%(username, messageToBreak[cutOffIndex:].lstrip())
        else:
            if messageToBreak.rstrip() != "@%s"%(username):
                messagesToSend.append(messageToBreak.rstrip())
            break
    return messagesToSend
