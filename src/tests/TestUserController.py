import unittest
from unittest.mock import Mock, patch
from datetime import timedelta, timezone, datetime
from ..controllers import UserController
from ..core.data import DataConfig
from ..core.user.User import User
import tweepy

class TwitterUser:
    def __init__(self, username):
        self.username = username


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), 1)
        self.mockUserDataStrategy = Mock()
        self.mockUserDataStrategyAttrs = {"saveUser.return_value": 1,
                "getUserByUsername.return_value": None,
                "getUserById.return_value": self.userToTest,
                "updateUser.return_value": True}
        self.mockUserDataStrategy.configure_mock(**self.mockUserDataStrategyAttrs)
        DataConfig.UserDataStrategy = self.mockUserDataStrategy

    @patch.object(tweepy.API, 'me')
    def test_userCanBeSaved(self, mePatch):
        mePatch.return_value(TwitterUser('example'))
        self.assertEqual(UserController.createUser('asd', '123fsd'), {"result": "success", "value": 1, "updated": False})
        self.assertTrue(self.mockUserDataStrategy.saveUser.called)
        self.assertTrue(mePatch.called)

    def test_userTimeZoneCanBeSet(self):
        formValue = {'tzhour': 5, 'tzminute': 30}
        userId = 1
        self.assertEqual(UserController.setTimeZone(formValue, userId),{"result": "success"})
        self.assertTrue(self.mockUserDataStrategy.updateUser.called, )

    def test_userTimezoneCanBeRetrievedAsDictionary(self):
        userDetailsToTest = UserController.getUserTimeZone(1)
        self.assertEqual(userDetailsToTest, {"hours": 5, "minutes": 30})
        self.userToTest.timeZone = timezone(timedelta(hours=-5, minutes=-30))
        userDetailsToTest = UserController.getUserTimeZone(1)
        self.assertEqual(userDetailsToTest, {"hours": -5, "minutes": -30})

if __name__ == "__main__":
    unittest.main()
