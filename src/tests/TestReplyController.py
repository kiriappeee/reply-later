import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from ..controllers import ReplyController
from ..core.user.User import User
from ..core.messager import *
from ..core.scheduler import Scheduler
from ..core.data import DataConfig

class TestReplyController(unittest.TestCase):
    def setUp(self):
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        self.mentionsToReturn = ['a'] * 10
        self.mockUserDataStrategy = Mock()
        self.mockUserDataStrategyAttrs = {"getUserById.return_value": userToTest 
}
        self.mockUserDataStrategy.configure_mock(**self.mockUserDataStrategyAttrs)
        
        self.mockReplyDataStrategy = Mock()
        self.mockReplyDataStrategyAttrs = {"saveReply.return_value": 1 }
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
        formData = dict([('message', '@example this is my first GUI based test.'), ('month', str(d.month)), ('hour', str(d.hour)), ('day', str(d.day)), ('tzminute', '30'), ('minute', str(d.minute)), ('tzhour', '5')])
        self.assertEqual(ReplyController.createReply(formData, '12345', 1), {"result": "success", "value": 1})
        self.assertTrue(self.mockReplyDataStrategy.saveReply.called)
        self.assertTrue(scheduleReplyPatch.called)
    
if __name__ == "__main__":
    unittest.main()
