import unittest
from copy import deepcopy
from unittest.mock import Mock
from datetime import timezone, timedelta, datetime, date
from ..reply.Reply import Reply
from ..reply import ReplyCRUD

class TestReply(unittest.TestCase):
    def test_replyObjectCreatesCorrectly(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30)))
        replyToTest = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(replyToTest.userId, 1)
        self.assertEqual(replyToTest.message, "@example an example message")
        self.assertEqual(replyToTest.scheduledTime, d)
        self.assertEqual(replyToTest.timeZone, timezone(timedelta(hours=5, minutes=30)))
        self.assertEqual(replyToTest.tweetId, 134953292)
        self.assertEqual(replyToTest.replyId, None)
        self.assertEqual(replyToTest.sentStatus, "unsent")
        replyToTest = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, sentStatus = "sent", replyId = 1)
        self.assertEqual(replyToTest.sentStatus, "sent")
        self.assertEqual(replyToTest.replyId, 1)

class TestReplyCRUD(unittest.TestCase):
    def test_replyObjectSavesCorrectly(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSave = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"saveReply.return_value": 1}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        self.assertEqual(ReplyCRUD.saveReply(replyToSave, mockReplyDataStrategy), {"result": "success", "value": 1})

    def test_replyObjectCannotBeSavedIfTimeIsBeforeCurrentTime(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) - timedelta(minutes=40)
        replyToSave = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        mockReplyDataStrategy = Mock()
        self.assertEqual(ReplyCRUD.saveReply(replyToSave, mockReplyDataStrategy), {"result": "error", "value": "Scheduled time cannot be earlier than current time"})

    def test_replyCanBeRetrievedById(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToRetrieve = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": replyToRetrieve}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        self.assertEqual(ReplyCRUD.getReplyByReplyId(1, mockReplyDataStrategy), replyToRetrieve)
        self.assertTrue(mockReplyDataStrategy.getReplyByReplyId.called)

    def test_replyCanBeUpdatedCorrectly(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToUpdate = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        newVersionOfReply = deepcopy(replyToUpdate)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": newVersionOfReply,
                "updateReply.return_value": True}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        replyToUpdate.message = "@example an updated message"
        self.assertEqual(ReplyCRUD.updateReply(replyToUpdate, mockReplyDataStrategy), {"result": "success"})

        newVersionOfReply.sentStatus = "sent"
        self.assertEqual(ReplyCRUD.updateReply(replyToUpdate, mockReplyDataStrategy), {"result": "error", "value": "Reply has already been sent"})
        
    def test_repliesCanBeCancelled(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToUpdate = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        newVersionOfReply = deepcopy(replyToUpdate)
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getReplyByReplyId.return_value": newVersionOfReply,
                "cancelReply.return_value": True, 
                }
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        self.assertEqual(ReplyCRUD.cancelReply(replyToUpdate, mockReplyDataStrategy), {"result": "success"})
        self.assertEqual(replyToUpdate.sentStatus, "cancelled")

    def test_repliesCanBeRetrievedByUserId(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replies = [
                Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1),
                Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 2)
                ]
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getRepliesByUserId.return_value": replies}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        self.assertEqual(ReplyCRUD.getRepliesByUserId(1, mockReplyDataStrategy), replies)

    def test_repliesCanBeRetrievedByUserIdAndStatus(self):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replies = [
                Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1),
                Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 2)
                ]
        mockReplyDataStrategy = Mock()
        mockReplyDataStrategyAttrs = {"getRepliesByUserIdAndStatus.return_value": replies}
        mockReplyDataStrategy.configure_mock(**mockReplyDataStrategyAttrs)
        self.assertEqual(ReplyCRUD.getRepliesByUserIdAndStatus(1, "unsent", mockReplyDataStrategy), replies)

if __name__ == "__main__":
    unittest.main()
