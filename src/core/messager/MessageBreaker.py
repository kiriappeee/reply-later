from . import TweetAdapter
from ttp import ttp
import re
def breakMessage(messageToBreak, tweetId, userId, userDataStrategy):
    if len(messageToBreak) <= 140:
        return [ messageToBreak ]
    username = TweetAdapter.getUsernameForTweet(tweetId, userId, userDataStrategy)
    splitMessageList = []
    urls = getUrls(messageToBreak)
    messageToBreak = transformMessageLinksToShortUrls(messageToBreak, urls)

    while messageToBreak!="":
        if len(messageToBreak) > 140:
            if messageToBreak[140] != " ":
                indexToSplitMessageAt = messageToBreak[0:140 + 1].rfind(" ")
            else:
                indexToSplitMessageAt = 140
            messageToAppend = messageToBreak[0:indexToSplitMessageAt].rstrip()
            messageToBreak = "@%s %s"%(username, messageToBreak[indexToSplitMessageAt:].lstrip())
            messageToAppend, urls = transformShortUrlsBackToOriginalLinks(messageToAppend, urls[:])
            splitMessageList.append(messageToAppend)

        else:
            if messageToBreak.rstrip() != "@%s"%(username):
                splitMessageList.append(messageToBreak.rstrip())
            break
    return splitMessageList

def transformShortUrlsBackToOriginalLinks(messageToTransform, urls):
    findUrlRegex = re.compile('http://short\.co[#]+')
    for foundUrl in findUrlRegex.findall(messageToTransform):
        messageToTransform = messageToTransform.replace(foundUrl, urls[0])
        urls.pop(0)
    return messageToTransform, urls

def getUrls(messageToParse):
    p = ttp.Parser()
    parsed = p.parse(messageToParse)
    urls = parsed.urls
    return urls

def transformMessageLinksToShortUrls(messageToBreak, urls):
    urlLength, urlLengthHttps = TweetAdapter.getUrlLengths()
    for url in urls:
        if url.startswith('https://'):
            lengthOfUrl = urlLengthHttps
        else:
            lengthOfUrl = urlLength
        messageToBreak = messageToBreak.replace(url, 'http://short.co'+'#'*(lengthOfUrl - 15))
    return messageToBreak
