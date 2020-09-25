import unittest
from email_setup import EmailSetup

class TestEmailSetup:
    def test_get_credentials(self):
        result = EmailSetup.get_credentials('test')

        self.assertIn(result, #, msg="Function, result: {result}, expected: {}")
