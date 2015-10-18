import unittest
import sqlite3

from datetime import timezone, timedelta
from ..core.user.User import User
from ..core.user import UserCRUD
from ..data.sqlite import UserDataStrategy
from . import ClearData

class TestSqliteUserDataStrategy(unittest.TestCase):
    def setUp(self):
        ClearData.clearData()
    def tearDown(self):
        ClearData.clearData()

    def test_userCanBeSaved(self):
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(UserCRUD.saveUser(userToTest, UserDataStrategy), {"result": "success", "value": 1})

    def test_userCanBeUpdated(self):
        userToTest = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(UserCRUD.saveUser(userToTest, UserDataStrategy), {"result": "success", "value": 1})
        userToTest = User('test', '123456-012e1asda', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)), userId = 1)
        self.assertEqual(UserCRUD.updateUser(userToTest, UserDataStrategy), {"result": "success"})
        userToTest = UserCRUD.getUserById(1, UserDataStrategy)
        self.assertEqual(userToTest.authToken, '123456-012e1asda')


    def test_userCanBeRetrieved(self):
        userToSave = User('test', '123456-012e1', '123h4123asdhh123', timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(UserCRUD.saveUser(userToSave, UserDataStrategy), {"result": "success", "value": 1})
        userToTest = UserCRUD.getUserById(1, UserDataStrategy)
        self.assertEqual(userToTest.username, 'test')
        self.assertEqual(userToTest.authToken, '123456-012e1')
        self.assertEqual(userToTest.secretToken, '123h4123asdhh123')
        self.assertEqual(userToTest.timeZone, timezone(timedelta(hours = 5, minutes = 30)))
        self.assertEqual(userToTest.userId, 1)

if __name__ == "__main__":
    unittest.main()
