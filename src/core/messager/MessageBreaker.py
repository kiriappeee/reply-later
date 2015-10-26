from . import TweetAdapter
from ttp import ttp
def breakMessage(messageToBreak, tweetId, userId, userDataStrategy):
    if len(messageToBreak) <= 140:
        return [ messageToBreak ]
    username = TweetAdapter.getUsernameForTweet(tweetId, userId, userDataStrategy)
    messagesToSend = []
    urlLength, urlLengthHttps = TweetAdapter.getUrlLengths()
    p = ttp.Parser()
    parsed = p.parse(messageToBreak)
    urls = parsed.urls
    while messageToBreak!="":
        if len(messageToBreak) > 140:
            endIndexToSearch = 140
            for url in urls:
                if messageToBreak.find(url) != -1:
                    if url.startswith('https://'):
                        if messageToBreak.find(url) < endIndexToSearch - urlLengthHttps:
                            endIndexToSearch = endIndexToSearch + urlLengthHttps
                    else:
                        if messageToBreak.find(url) < endIndexToSearch - urlLength:
                            endIndexToSearch = endIndexToSearch + urlLength
            if messageToBreak[endIndexToSearch] != " ":
                cutOffIndex = messageToBreak[0:endIndexToSearch + 1].rfind(" ")
            else:
                cutOffIndex = endIndexToSearch
            messagesToSend.append(messageToBreak[:cutOffIndex].rstrip())
            
            messageToBreak = "@%s %s"%(username, messageToBreak[cutOffIndex:].lstrip())
        else:
            if messageToBreak.rstrip() != "@%s"%(username):
                messagesToSend.append(messageToBreak.rstrip())
            break
    return messagesToSend
