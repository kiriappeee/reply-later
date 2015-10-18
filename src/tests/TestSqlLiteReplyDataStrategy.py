import unittest
from unittest.mock import Mock, patch
import sqlite3

from datetime import timezone, timedelta, datetime
from ..core.user.User import User
from ..core.reply.Reply import Reply
from ..core.reply import ReplyCRUD
from ..data.sqlite import ReplyDataStrategy
from ..core.scheduler import Scheduler
from . import ClearData

class TestSqliteReplyDataStrategy(unittest.TestCase):
    def setUp(self):
        ClearData.clearData()
    def tearDown(self):
        #ClearData.clearData()
        pass

    @patch.object(Scheduler, 'scheduleReply')
    def test_replyCanBeSaved(self, scheduleReplyPatch):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSave = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(ReplyCRUD.saveReply(replyToSave, ReplyDataStrategy), {"result": "success", "value": 1})
        
    @patch.object(Scheduler, 'scheduleReply')
    def test_replyCanBeRetrievedById(self, scheduleReplyPatch):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSave = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(ReplyCRUD.saveReply(replyToSave, ReplyDataStrategy), {"result": "success", "value": 1})
        replyToTest = ReplyCRUD.getReplyByReplyId(1, ReplyDataStrategy)
        self.assertEqual(replyToTest.userId, 1)
        self.assertEqual(replyToTest.message, "@example an example message")
        self.assertEqual(replyToTest.scheduledTime, d)
        self.assertEqual(replyToTest.timeZone, timezone(timedelta(hours=5, minutes=30)))
        self.assertEqual(replyToTest.tweetId, '134953292')
        self.assertEqual(replyToTest.replyId, 1)

    @patch.object(Scheduler, 'scheduleReply')
    @patch.object(Scheduler, 'updateReply')
    @patch.object(Scheduler, 'removeReply')
    def test_replyCanBeUpdated(self, removeReplyPatch, scheduleReplyPatch, updateReplyPatch):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        replyToSave = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(ReplyCRUD.saveReply(replyToSave, ReplyDataStrategy), {"result": "success", "value": 1})
        replyToUpdate = Reply(1, "@example an example message please", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        self.assertEqual(ReplyCRUD.updateReply(replyToUpdate, ReplyDataStrategy), {"result": "success"})
        replyToTest = ReplyCRUD.getReplyByReplyId(1, ReplyDataStrategy)
        self.assertEqual(replyToTest.message, "@example an example message please")

    @patch.object(Scheduler, 'scheduleReply')
    @patch.object(Scheduler, 'updateReply')
    @patch.object(Scheduler, 'removeReply')
    def test_replyCanBeCancelled(self, removeReplyPatch, scheduleReplyPatch, updateReplyPatch):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        reply = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 1})
        reply.replyId = 1
        self.assertEqual(ReplyCRUD.cancelReply(reply, ReplyDataStrategy), {"result": "success"})
        replyToTest = ReplyCRUD.getReplyByReplyId(1, ReplyDataStrategy)
        self.assertEqual(replyToTest.sentStatus, "cancelled")

    @patch.object(Scheduler, 'scheduleReply')
    def test_repliesCanBeRetrievedByUserId(self, scheduleReplyPatch):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        reply = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 1})
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 2})
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 3})
        reply.userId = 2
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 4})
        repliesToTest = ReplyCRUD.getRepliesByUserId(1, ReplyDataStrategy)
        self.assertEqual(len(repliesToTest), 3)

    @patch.object(Scheduler, 'scheduleReply')
    def test_repliesCanBeRetrievedByUserIdAndStatus(self, scheduleReplyPatch):
        d = datetime.now(tz = timezone(timedelta(hours=5, minutes=30))) + timedelta(minutes=20)
        reply = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292)
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 1})
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 2})
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 3})
        reply.userId = 2
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 4})
        reply.userId = 1
        reply.sentStatus = "sent"
        self.assertEqual(ReplyCRUD.saveReply(reply, ReplyDataStrategy), {"result": "success", "value": 5})
        repliesToTest = ReplyCRUD.getRepliesByUserIdAndStatus(1, "unsent", ReplyDataStrategy)
        self.assertEqual(len(repliesToTest), 3)
        repliesToTest = ReplyCRUD.getRepliesByUserIdAndStatus(1, "sent", ReplyDataStrategy)
        self.assertEqual(len(repliesToTest), 1)
        repliesToTest = ReplyCRUD.getRepliesByUserIdAndStatus(2, "sent", ReplyDataStrategy)
        self.assertEqual(len(repliesToTest), 0)

if __name__ == "__main__":
    unittest.main()
