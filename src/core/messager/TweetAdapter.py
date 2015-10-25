import tweepy
from tweepy.error import TweepError
import configparser
from urllib import parse

from ..user import UserCRUD

PATH_TO_CONFIG = 'src/tweetconfig.ini'
def getUsernameForTweet(tweetId, userId, userDataStrategy):
    api = getApi(userId, userDataStrategy)
    tweet = api.get_status(tweetId)
    username = tweet.user.screen_name
    return username

def sendReply(replyMessage, replyId, userId, userDataStrategy):
    api = getApi(userId, userDataStrategy)
    tweet = api.update_status(replyMessage, replyId)
    return tweet.id

def getSingleTweet(tweetIdOrUrl, userId, userDataStrategy):
    api = getApi(userId, userDataStrategy)
    tweetId = ""
    if tweetIdOrUrl.find('/') == -1:
        tweetId = tweetIdOrUrl
    else:
        tweetId = parse.urlparse(tweetIdOrUrl).path.split('/')[-1]

    try:
        tweetToReturn = api.get_status(tweetId)
        return tweetToReturn
    except TweepError as err:
        if err.reason.find("status code = 404") > -1:
            return "No such tweet"
        else:
            return err.reason
    
def getApi(userId, userDataStrategy):
    global PATH_TO_CONFIG
    user = UserCRUD.getUserById(userId, userDataStrategy)
    config = configparser.ConfigParser()
    config.read(PATH_TO_CONFIG)
    consumer_key = config['TOKEN']['consumerKey']
    consumer_secret = config['TOKEN']['consumerSecret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(user.authToken, user.secretToken)
    api = tweepy.API(auth)
    return api

def createAPIObject():
    global PATH_TO_CONFIG
    config = configparser.ConfigParser()
    config.read(PATH_TO_CONFIG)
    consumer_key = config['TOKEN']['consumerKey']
    consumer_secret = config['TOKEN']['consumerSecret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    return api

def getMentions(userId, count, userDataStrategy):
    api = getApi(userId, userDataStrategy)
    mentions = api.mentions_timeline(count=count)
    return mentions

def getUrlLengths():
    api = createAPIObject()
    configValues = api.configuration()
    return configValues['short_url_length'], configValues['short_url_length_https']
