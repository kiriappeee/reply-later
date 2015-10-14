from . import TweetAdapter
def breakMessage(messageToBreak, tweetId):
    if len(messageToBreak) <= 140:
        return [ messageToBreak ]
    username = TweetAdapter.getUsernameForTweet(tweetId)
    messagesToSend = []
    messagesToSend.append(messageToBreak[:140])
    messageToBreak = "@%s %s"%(username, messageToBreak[140:].lstrip())
    while messageToBreak!="":
        if len(messageToBreak) > 140:
            if messageToBreak[139] != " ":
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
