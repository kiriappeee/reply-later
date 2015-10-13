import unittest
from unittest.mock import Mock
from datetime import timezone, timedelta
from ..user.User import User
from ..user import UserCRUD

class TestUsers(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_userObjectCreatesCorrectly(self):
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(userToTest.username, 'test')
        self.assertEqual(userToTest.authToken, '123456-012e1')
        self.assertEqual(userToTest.secretToken, '123h4123asdhh123')
        self.assertEqual(userToTest.timeZone, timezone(timedelta(hours = 5, minutes = 30)))
        self.assertIsNone(userToTest.userId)

    def test_validUserCanBeSaved(self):
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"saveUser.return_value": 1}
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(UserCRUD.saveUser(userToTest, mockUserDataStrategy), {"result": "success", "value": 1})

    def test_invalidUserReturnsError(self):
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"saveUser.return_value": 1}
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        userToTest = User('', '', '', None)
        self.assertEqual(UserCRUD.saveUser(userToTest, mockUserDataStrategy), {"result": "error", "value": {"tokenError": "Token cannot be empty", "secretError": "Secret cannot be empty", "usernameError": "Username cannot be empty"}})

    def test_userCanBeEdited(self):
        mockUserDataStrategy = Mock()
        mockUserDataStrategyAttrs = {"saveUser.return_value": 1,
                "updateUser.return_value": True}
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        self.assertEqual(UserCRUD.updateUser(userToTest, mockUserDataStrategy), {"result": "success"})
        userToTest = User('test', '', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        self.assertEqual(UserCRUD.updateUser(userToTest, mockUserDataStrategy), {"result": "error", "value": {"tokenError": "Token cannot be empty"}})


if __name__ == "__main__":
    unittest.main()
