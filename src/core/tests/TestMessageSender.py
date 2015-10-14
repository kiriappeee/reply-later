import unittest
from unittest.mock import Mock, patch
from datetime import timezone, timedelta, datetime
from ..reply.Reply import Reply
from ..reply import ReplyCRUD
from ..messager import TweetAdapter, MessageBreaker

class TestMessageSender(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    #example of how to patch a class
    """
    @patch('tweepy.API.update_status')
    def test_tweetLibraryCanBePatched(self, patchClass):
        patchClass.return_value = "success"
        self.assertTrue(True)
        self.assertEqual(TweetAdapter.updateStatus("abc", "bad"), "success")
        self.assertEqual(patchClass.call_args[0], ("abc", "bad"))
    """

    def test_messageIsBrokenDownCorrectlyBeforeSending(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId), ["@example an example message"])

    @patch.object(TweetAdapter, 'getUsernameForTweet')
    def test_messageIsBrokenDownCorrectlyWhenMoreThan140Chars(self, patchMethod):
        patchMethod.return_value = "example"
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, 
                "@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3 tweets long so that I can make sure that the module is working properly. Like really well.",
                d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId), ["@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little",
            "@example messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3",
            "@example tweets long so that I can make sure that the module is working properly. Like really well."])

if __name__ == "__main__":
    unittest.main()
