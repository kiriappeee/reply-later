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

if __name__ == "__main__":
    unittest.main()
