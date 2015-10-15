import unittest
from unittest.mock import Mock, patch
from datetime import timezone, timedelta, datetime
from ..reply.Reply import Reply
from ..reply import ReplyCRUD
from ..user.User import User
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
        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId, 1, mockUserDataStrategy), ["@example an example message"])

    @patch.object(TweetAdapter, 'getUsernameForTweet')
    def test_messageIsBrokenDownCorrectlyWhenMoreThan140Chars(self, patchMethod):
        patchMethod.return_value = "example"
        
        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, 
                "@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3 tweets long so that I can make sure that the module is working properly. Like really well.",
                d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)

        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId, 1, mockUserDataStrategy), ["@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little",
            "@example messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3",
            "@example tweets long so that I can make sure that the module is working properly. Like really well."])
        patchMethod.assert_any_call(134953292, 1, mockUserDataStrategy)

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
        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        DataConfig.UserDataStrategy = mockUserDataStrategy
        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})
        usernameMethod.assert_not_called()
        sendReplyPatch.assert_called_once_with("@example an example message", 134953292, 1, mockUserDataStrategy)

    @patch.object(TweetAdapter, 'getUsernameForTweet')
    @patch.object(TweetAdapter, 'sendReply')
    def test_messageIsSentCorrectlyWhenOver140Chars(self, sendReplyPatch, usernameMethod):
        sendReplyPatch.side_effect = [1234, 1235, 1236]
        usernameMethod.return_value = "example"

        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, 
                "@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3 tweets long so that I can make sure that the module is working properly. Like really well.",
                d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)

        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": replyToSend}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        DataConfig.UserDataStrategy = mockUserDataStrategy
        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234, 1235, 1236]}})
        usernameMethod.assert_called_once_with(134953292, 1, mockUserDataStrategy)
        t1 = "@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little"
        t2 = "@example messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3"
        t3 = "@example tweets long so that I can make sure that the module is working properly. Like really well."
        sendReplyPatch.assert_any_call(t1, 134953292, 1, mockUserDataStrategy)
        sendReplyPatch.assert_any_call(t2, 1234, 1, mockUserDataStrategy)
        sendReplyPatch.assert_any_call(t3, 1235, 1, mockUserDataStrategy)


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
