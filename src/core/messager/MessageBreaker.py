from . import TweetAdapter
from ttp import ttp
import re
def breakMessage(messageToBreak, tweetId, userId, userDataStrategy):
    if len(messageToBreak) <= 140:
        return [ messageToBreak ]
    username = TweetAdapter.getUsernameForTweet(tweetId, userId, userDataStrategy)
    messagesToSend = []
    findUrlRegex = re.compile('http://short\.co[#]+')
    urls = getUrls(messageToBreak)
    messageToBreak = replaceUrlsInMessageWithShortUrls(messageToBreak, urls)

    while messageToBreak!="":
        if len(messageToBreak) > 140:
            if messageToBreak[140] != " ":
                cutOffIndex = messageToBreak[0:140 + 1].rfind(" ")
            else:
                cutOffIndex = 140
            messageToAppend = messageToBreak[0:cutOffIndex].rstrip()
            messageToBreak = "@%s %s"%(username, messageToBreak[cutOffIndex:].lstrip())
            for foundUrl in findUrlRegex.findall(messageToAppend):
                messageToAppend = messageToAppend.replace(foundUrl, urls[0])
                urls.pop(0)
            
            messagesToSend.append(messageToAppend)
            
        else:
            if messageToBreak.rstrip() != "@%s"%(username):
                messagesToSend.append(messageToBreak.rstrip())
            break
    return messagesToSend

def getUrls(messageToParse):
    p = ttp.Parser()
    parsed = p.parse(messageToParse)
    urls = parsed.urls
    return urls

def replaceUrlsInMessageWithShortUrls(messageToBreak, urls):
    urlLength, urlLengthHttps = TweetAdapter.getUrlLengths()
    for url in urls:
        if url.startswith('https://'):
            lengthOfUrl = urlLengthHttps
        else:
            lengthOfUrl = urlLength
        messageToBreak = messageToBreak.replace(url, 'http://short.co'+'#'*(lengthOfUrl - 15))
    return messageToBreak
