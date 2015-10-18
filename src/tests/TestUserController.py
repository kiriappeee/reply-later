import unittest
from unittest.mock import Mock, patch
from ..controllers import UserController
from ..core.data import DataConfig
import tweepy

class TwitterUser:
    def __init__(self, username):
        self.username = username


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.mockUserDataStrategy = Mock()
        self.mockUserDataStrategyAttrs = {"saveUser.return_value": 1,
                "updateUser.return_value": True}
        self.mockUserDataStrategy.configure_mock(**self.mockUserDataStrategyAttrs)
        DataConfig.UserDataStrategy = self.mockUserDataStrategy

    @patch.object(tweepy.API, 'me')
    def test_userCanBeSaved(self, mePatch):
        mePatch.return_value(TwitterUser('example'))
        self.assertEqual(UserController.createUser('asd', '123fsd'), {"result": "success", "value": 1})
        self.assertTrue(self.mockUserDataStrategy.saveUser.called)
        self.assertTrue(mePatch.called)

    def test_userTimeZoneCanBeSet(self):
        formValue = {'tzhour': 5, 'tzminute': 30}
        userId = 1
        self.assertEqual(UserController.setTimeZone(formValue, userId),{"result": "success"})
        self.assertTrue(self.mockUserDataStrategy.updateUser.called, )



if __name__ == "__main__":
    unittest.main()
