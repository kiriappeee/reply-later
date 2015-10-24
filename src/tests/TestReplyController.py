import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from ..controllers import ReplyController
from ..core.user.User import User
from ..core.reply.Reply import Reply
from ..core.messager import *
from ..core.scheduler import Scheduler
from ..core.data import DataConfig
from ..core.scheduler import Scheduler

class TestReplyController(unittest.TestCase):
    def setUp(self):
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        self.mentionsToReturn = ['a'] * 10
        self.d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30)))
        self.repliesToReturn = [
                Reply(1, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =1),
                Reply(1, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =2),
                Reply(1, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =3), 
                Reply(2, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =4), 
                Reply(2, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =5), 
                Reply(1, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =6, sentStatus="sent"), 
                Reply(1, "@example an example message", self.d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId =7, sentStatus="cancelled"), 
                ]

        def returnReplies(userId, status=""):
            if status == "":
                return [reply for reply in self.repliesToReturn if reply.userId == userId]
            else:
                return [reply for reply in self.repliesToReturn if reply.userId == userId and reply.sentStatus == status]

        self.mockUserDataStrategy = Mock()
        self.mockUserDataStrategyAttrs = {"getUserById.return_value": userToTest 
}
        self.mockUserDataStrategy.configure_mock(**self.mockUserDataStrategyAttrs)
        
        self.mockReplyDataStrategy = Mock()
        self.mockReplyDataStrategyAttrs = {"saveReply.return_value": 1,
                "getRepliesByUserId.side_effect": returnReplies,
                "getReplyByReplyId.return_value": self.repliesToReturn[1],
                "getRepliesByUserIdAndStatus.side_effect": returnReplies,
                "cancelReply.return_value": True}
        self.mockReplyDataStrategy.configure_mock(**self.mockReplyDataStrategyAttrs)
        DataConfig.UserDataStrategy = self.mockUserDataStrategy
        DataConfig.ReplyDataStrategy = self.mockReplyDataStrategy



    def tearDown(self):
        pass

    @patch.object(TweetAdapter, 'getMentions')
    def test_mentionsCanBeRetrieved(self, mentionsPatch):
        mentionsPatch.return_value = self.mentionsToReturn
        mentionList = ReplyController.getMentions(1)
        self.assertEqual(self.mentionsToReturn, mentionList)

    @patch.object(Scheduler, 'scheduleReply')
    def test_repliesCanBeScheduled(self, scheduleReplyPatch):
        d = datetime.now(tz=timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=2)
        formData = dict([('message', '@example this is my first GUI based test.'), ('month', str(d.month)), ('hour', str(d.hour)), ('day', str(d.day)), ('tzminute', '30'), ('minute', str(d.minute)), ('tzhour', '5'), ('tweetId', '12345')])
        self.assertEqual(ReplyController.createReply(formData, 1), {"result": "success", "value": 1})
        self.assertTrue(self.mockReplyDataStrategy.saveReply.called)
        self.assertTrue(scheduleReplyPatch.called)
    
    @patch.object(TweetAdapter, 'getSingleTweet')
    def test_singleTweetcanBeRetrieved(self, tweetPatch):
        tweetPatch.return_value = self.mentionsToReturn[0]
        tweetToObtain = ReplyController.getTweet("1234", 1)
        self.assertEqual(tweetToObtain, self.mentionsToReturn[0])

    def test_allScheduledItemsCanBeRetrieved(self):
        replies = ReplyController.getScheduledReplies(1, "all")
        self.assertEqual(len(replies), 5)
        replies = ReplyController.getScheduledReplies(1, "unsent")
        self.assertEqual(len(replies), 3)
        self.assertEqual(replies[0], {"reply": self.repliesToReturn[0], "timeZoneInformation": {"minutes": 30, "hours": 5}})
        replies = ReplyController.getScheduledReplies(1, "cancelled")
        self.assertEqual(len(replies), 1)
        replies = ReplyController.getScheduledReplies(1, "sent")
        self.assertEqual(len(replies), 1)
        replies = ReplyController.getScheduledReplies(2, "sent")
        self.assertEqual(len(replies), 0)

    def test_singleReplyInfoRetrieved(self):
        reply = ReplyController.getSingleReply(1,2)
        self.assertEqual(reply, {"reply": self.repliesToReturn[1], "timeZoneInformation": {"minutes": 30, "hours": 5}})
        reply = ReplyController.getSingleReply(2,2)
        self.assertEqual(reply, {"reply": None, "reason": "You do not have permission to view this"})

    @patch.object(Scheduler, 'removeReply')
    def test_scheduledReplyCanBeCancelled(self, removeReplyPatch):
        self.repliesToReturn[1].scheduledTime = self.d + timedelta(minutes=10)
        cancelResult = ReplyController.cancelReply(1,1)
        self.assertEqual(cancelResult, {"result": "success"})
        cancelResult = ReplyController.cancelReply(2,1)
        self.assertEqual(cancelResult, {"result": "error", "reason": "You do not have permission to perform this action"})

    @patch.object(Scheduler, 'updateReply')
    def test_scheduledReplyCanBeUpdated(self, updateReplyPatch):
        updatedTime = self.d + timedelta(minutes=10)
        formData = dict([('message', '@example this is my first GUI based test.'), ('month', str(updatedTime.month)), ('hour', str(updatedTime.hour)), ('day', str(updatedTime.day)), ('tzminute', '30'), ('minute', str(updatedTime.minute)), ('tzhour', '5'), ('tweetId', '12345'), ('replyid', '1')])
        updateResult = ReplyController.updateReply(1, formData)
        self.assertEqual(updateResult, {"result": "success"})
        updateResult = ReplyController.updateReply(2, formData)
        self.assertEqual(updateResult, {"result": "error", "reason": "You do not have permission to perform this action"})

if __name__ == "__main__":
    unittest.main()
