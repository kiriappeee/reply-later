import unittest
from unittest.mock import Mock, patch
from datetime import timezone, timedelta, datetime
from ..reply.Reply import Reply
from ..reply import ReplyCRUD
from ..messager import TweetAdapter, MessageBreaker, MessageSender
from ..data import DataConfig

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

    @patch.object(TweetAdapter, 'getUsernameForTweet')
    @patch.object(TweetAdapter, 'sendReply')
    def test_messageIsSentCorrectlyWhenUnder140Chars(self, sendReplyPatch, usernameMethod):
        sendReplyPatch.side_effect = [1234]
        usernameMethod.return_value = "example"
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": replyToSend}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})

    @patch.object(TweetAdapter, 'getUsernameForTweet')
    @patch.object(TweetAdapter, 'sendReply')
    def test_messageIsSentCorrectlyWhenOver140Chars(self, sendReplyPatch, usernameMethod):
        sendReplyPatch.side_effect = [1234, 1235, 1236]
        usernameMethod.return_value = "example"

        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, 
                "@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3 tweets long so that I can make sure that the module is working properly. Like really well.",
                d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)

        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": replyToSend}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234, 1235, 1236]}})
        print(sendReplyPatch.call_args_list)

    @patch.object(TweetAdapter, 'sendReply')
    def test_messageStatusIsChangedAndSavedAfterSending(self, sendReplyPatch):
        sendReplyPatch.return_value = 1234
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": replyToSend,
                "saveReply.return_value": True}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        with patch.object(ReplyCRUD, 'saveReply', return_value={"result": "success"}) as saveReplyPatch:
            self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})
            self.assertEqual(replyToSend.sentStatus, "sent")
            saveReplyPatch.assert_called_once_with(replyToSend, mockReplyDataStrategy)

        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})
        self.assertEqual(replyToSend.sentStatus, "sent")
        mockReplyDataStrategy.saveReply.assert_called_once_with(replyToSend)

if __name__ == "__main__":
    unittest.main()
