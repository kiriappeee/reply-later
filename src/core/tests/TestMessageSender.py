import unittest
from unittest.mock import Mock, patch
import copy
from datetime import timezone, timedelta, datetime
from ..reply.Reply import Reply
from ..reply import ReplyCRUD
from ..user.User import User
from ..messager import TweetAdapter, MessageBreaker, MessageSender
from ..data import DataConfig
from ..scheduler import Scheduler

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

    @patch.object(TweetAdapter, 'getUrlLengths')
    @patch.object(TweetAdapter, 'getUsernameForTweet')
    def test_messageIsBrokenDownCorrectlyBeforeSendingWhenContainingLinks(self, patchMethod, urlLengthPatch):
        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        patchMethod.return_value = "example"
        urlLengthPatch.return_value = (23,23)
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "... Facebook biased - when did people give up on the process of getting informed? http://blog.theoldreader.com/post/144197778539/facebook-biased via @theoldreader", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId, 1, mockUserDataStrategy), ["... Facebook biased - when did people give up on the process of getting informed? http://blog.theoldreader.com/post/144197778539/facebook-biased via @theoldreader"])
        
    @patch.object(TweetAdapter, 'getUrlLengths')
    @patch.object(TweetAdapter, 'getUsernameForTweet')
    def test_messageIsBrokenDownCorrectlyWhenMoreThan140Chars(self, patchMethod, urlLengthPatch):
        patchMethod.return_value = "example"
        urlLengthPatch.return_value = (23,23)
        
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
        replyToSend.message = "@example testing what happens to long tweets with links. There are 50 characters here that I will insert now I'm just interested in seeing what gets truncated after 140 characters"
        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId, 1, mockUserDataStrategy),
                ["@example testing what happens to long tweets with links. There are 50 characters here that I will insert now I'm just interested in seeing", "@example what gets truncated after 140 characters"])

    @patch.object(TweetAdapter, 'getUrlLengths')
    @patch.object(TweetAdapter, 'getUsernameForTweet')
    def test_messageIsBrokenDownCorrectlyWhenMoreThan140CharsAndContainsLinks(self, patchMethod, urlLengthPatch):
        patchMethod.return_value = "example"
        urlLengthPatch.return_value = (23,23)
        
        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, 
                "@example an example message that is just way too long to be kept inside a single tweet. It also contains a link to http://replylater.adnanissadeen.com that should become shortened. Therefore it will be broken down into lots of little messages each having the example username on top of it. Sounds cool? Keep going! Throw in one more link like https://blog.bufferapp.com/twitter-polls for good measure (also, https). I'd really like to make this message more than 3 tweets long so that I can make sure that the module is working properly. Like really well.",
                d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)

        m1 = "@example an example message that is just way too long to be kept inside a single tweet. It also contains a link to http://replylater.adnanissadeen.com"
        m2 = "@example that should become shortened. Therefore it will be broken down into lots of little messages each having the example username on top"
        m3 = "@example of it. Sounds cool? Keep going! Throw in one more link like https://blog.bufferapp.com/twitter-polls for good measure (also, https). I'd really like"
        m4 = "@example to make this message more than 3 tweets long so that I can make sure that the module is working properly. Like really well."
        self.assertEqual(MessageBreaker.breakMessage(replyToSend.message, replyToSend.tweetId, 1, mockUserDataStrategy), [m1,m2,m3,m4])
        patchMethod.assert_any_call(134953292, 1, mockUserDataStrategy)
        
    @patch.object(TweetAdapter, 'getUrlLengths')
    @patch.object(TweetAdapter, 'getUsernameForTweet')
    @patch.object(TweetAdapter, 'sendReply')
    def test_messageIsSentCorrectlyWhenUnder140Chars(self, sendReplyPatch, usernameMethod, urlLengthPatch):
        sendReplyPatch.side_effect = [1234]
        urlLengthPatch.return_value = (23,23)
        usernameMethod.return_value = "example"
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.side_effect": [copy.deepcopy(replyToSend), copy.deepcopy(replyToSend)]}
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

    @patch.object(TweetAdapter, 'getUrlLengths')
    @patch.object(TweetAdapter, 'getUsernameForTweet')
    @patch.object(TweetAdapter, 'sendReply')
    def test_messageIsSentCorrectlyWhenOver140Chars(self, sendReplyPatch, usernameMethod, urlLengthPatch):
        sendReplyPatch.side_effect = [1234, 1235, 1236]
        urlLengthPatch.return_value = (23,23)
        usernameMethod.return_value = "example"

        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) 
        replyToSend = Reply(1, 
                "@example an example message that is just way too long to be kept inside a single tweet. Therefore it will be broken down into lots of little messages each having the example username on top of it. Sounds cool? Keep going! I'd really like to make this message about 3 tweets long so that I can make sure that the module is working properly. Like really well.",
                d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)

        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"getUserById.return_value": user }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.side_effect": [copy.deepcopy(replyToSend), copy.deepcopy(replyToSend)]}
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
        self.assertTrue(mockReplyDataStrategy.updateReply.called)


    @patch.object(TweetAdapter, 'sendReply')
    def test_messageStatusIsChangedAndSavedAfterSending(self, sendReplyPatch):
        sendReplyPatch.return_value = 1234
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        repliesToCheck = [copy.deepcopy(replyToSend), copy.deepcopy(replyToSend), copy.deepcopy(replyToSend)]
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.side_effect": repliesToCheck,
                "updateReply.return_value": True}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        with patch.object(ReplyCRUD, 'updateReply', return_value={"result": "success"}) as saveReplyPatch:
            self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})
            saveReplyPatch.assert_called_once_with(repliesToCheck[0], mockReplyDataStrategy)

        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})
        self.assertEqual(repliesToCheck[1].sentStatus, "sent")
        mockReplyDataStrategy.updateReply.assert_called_once_with(repliesToCheck[1])

    @patch.object(TweetAdapter, 'sendReply')
    @patch.object(Scheduler, 'removeReply')
    def test_messageIsRemovedFromSchedulerAfterSending(self, schedulePatch, sendReplyPatch):
        sendReplyPatch.return_value = 1234
        schedulePatch.return_value = None
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSend = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        repliesToCheck = [copy.deepcopy(replyToSend), copy.deepcopy(replyToSend), copy.deepcopy(replyToSend)]
        user = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.side_effect": repliesToCheck,
                "updateReply.return_value": True}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        DataConfig.ReplyDataStrategy = mockReplyDataStrategy
        self.assertEqual(MessageSender.sendMessage(1, ""), {"result": "success", "value": {"tweets": [1234]}})
        schedulePatch.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
