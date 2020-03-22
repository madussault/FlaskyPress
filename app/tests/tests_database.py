"""Tests the existence of our database.

To run this particular test file use the following command line:

nose2 -v app.tests.tests_database
"""

from app import create_app
from unittest import TestCase
import unittest
import os
from config import Config


class TestConfig(Config):
    """Custom configuration for our tests.

    Attributes
    ----------
    TESTING : bool
        Enable testing mode. Exceptions are propagated rather than handled by
        the app’s error handlers.
        Must be set to True to prevent the mail logger from sending email
        warnings.
    """
    TESTING = True


class Database(TestCase):
    """Contains the tests to verify the existence of our database.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_database_existence(self):
        """Ensure that the production database exists.
        """
        tester = os.path.exists("blog.db")
        self.assertTrue(tester, "The database file can not be found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
