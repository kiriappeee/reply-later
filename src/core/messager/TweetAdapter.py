import tweepy
import configparser
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
