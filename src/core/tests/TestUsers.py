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
        mockUserDataStrategyAttrs = {"saveUser.return_value": 1,
                "getUserByUsername.return_value": None
                }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(UserCRUD.saveUser(userToTest, mockUserDataStrategy), {"result": "success", "value": 1, "updated": False})

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

    def test_userCanBeRetrieved(self):
        mockUserDataStrategy = Mock()
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        mockUserDataStrategyAttrs = {"getUserById.return_value": userToTest
                }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        self.assertEqual(UserCRUD.getUserById(1, mockUserDataStrategy), userToTest)

    def test_userCanBeRetrievedByUsername(self):
        mockUserDataStrategy = Mock()
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        mockUserDataStrategyAttrs = {"getUserByUsername.return_value": userToTest
                }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        self.assertEqual(UserCRUD.getUserByUsername('test', mockUserDataStrategy), userToTest)
        mockUserDataStrategy.getUserByUsername.assert_called_once_with('test')

    def test_userIsUpdatedInsteadOfSavingIfUserExists(self):
        mockUserDataStrategy = Mock()
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        userToSave = User('test', '1231lkjasd-12a', 'p99087676dsaanbwU', timezone(timedelta(hours = 0, minutes = 0)))
        mockUserDataStrategyAttrs = {"getUserByUsername.return_value": userToTest,
                "updateUser.return_value": True
                }
        mockUserDataStrategy.configure_mock(**mockUserDataStrategyAttrs)
        self.assertEqual(UserCRUD.saveUser(userToSave, mockUserDataStrategy), {"result": "success", "value": 1, "updated": True})
        self.assertTrue(mockUserDataStrategy.updateUser.called)
        self.assertEqual(userToSave.timeZone, userToTest.timeZone)
        mockUserDataStrategy.getUserByUsername.assert_called_once_with('test')

if __name__ == "__main__":
    unittest.main()
