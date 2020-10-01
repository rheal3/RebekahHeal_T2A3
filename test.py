import unittest
from groups import Groups
from user import User


class TestGroup(unittest.TestCase):
    def test_day_validation(self):
        result = Groups.day_validation({'group': 'friends', 'days': '3'}, '3')
        self.assertEqual(result, True, msg=f"day_validation('3'), result: \
{result}, expected: True")


class TestUser(unittest.TestCase):
    def test_check_hashed_pass(self):
        stored = "$2b$12$1bus67Xcg2y/KZor5BuTUuCCop9gJIZSL2kmEmNMT7oMVnl\
GKrrTS".encode('utf8')
        test_pass = User.hash_password('test')
        result = User.check_hashed_pass(test_pass.encode('utf8'), stored)
        self.assertEqual(result, False, msg=f"hash_password('test'), result: \
{result}, expected: False")
