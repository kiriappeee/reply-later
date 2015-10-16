import unittest
from unittest.mock import Mock
import configparser
from datetime import timezone, timedelta, datetime

import tweepy

from ..messager import TweetAdapter
from ..user.User import User


class SlowTests(unittest.TestCase):
    def setUp(self):
        PATH_TO_CONFIG = 'src/tweetconfig.ini'
        config = configparser.ConfigParser()
        config.read(PATH_TO_CONFIG)
        consumer_key = config['TOKEN']['consumerKey']
        consumer_secret = config['TOKEN']['consumerSecret']
        self.user = User("kiriappee", config['TOKEN']['devAccessToken'],
                config['TOKEN']['devAccessSecret'],
                timezone(timedelta(hours=5, minutes=30)),
                userId = 1)
        self.mockUserDataStrategy= Mock()
        self.mockUserDataStrategyAttrs = {"getUserById.return_value": self.user }
        self.mockUserDataStrategy.configure_mock(**self.mockUserDataStrategyAttrs)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(self.user.authToken, self.user.secretToken)
        self.api = tweepy.API(auth)

    def test_canRetrieveUsernameForTweet(self):
        username = TweetAdapter.getUsernameForTweet('653401595762225152', 1, self.mockUserDataStrategy)
        self.assertEqual(username, "area51research")

    def test_replyCanBeSent(self):
        tweetId = TweetAdapter.sendReply("@area51research this is a test", '653401595762225152', 1, self.mockUserDataStrategy)
        print(tweetId)
        self.assertIsNotNone(tweetId)
        self.api.destroy_status(id=tweetId)
    def test_mentionListCanBeObtained(self):
        self.assertEqual(len(TweetAdapter.getMentions(1, 30, self.mockUserDataStrategy)),30)

class FastTests(unittest.TestCase):

    def test_canGetGenericAPIObject(self):
        self.assertIsNotNone(TweetAdapter.createAPIObject())
if __name__ == "__main__":
    unittest.main()
