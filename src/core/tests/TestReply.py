import unittest
from datetime import timezone, timedelta, datetime, date
from ..reply.Reply import Reply

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
        replyToTest = Reply(1, "@example an example message", d, timezone(timedelta(hours=5, minutes=30)), 134953292, replyId = 1)
        self.assertEqual(replyToTest.replyId, 1)

if __name__ == "__main__":
    unittest.main()
