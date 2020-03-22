"""Testing the functions inside the initialisation file of the ``main``
package.

To run this particular test file use the following command line:

nose2 -v app.tests.main.tests_init
"""
from app import create_app
import unittest
from unittest import TestCase
from config import Config, basedir
import os
from app.main import create_db

db_path = os.path.join(basedir, 'test.db')


class TestConfig(Config):
    """Custom configuration for our tests.

    Attributes
    ----------
    TESTING : bool
        Enable testing mode. Exceptions are propagated rather than handled by
        the app’s error handlers.
        Must be set to True to prevent the mail logger from sending email
        warnings.
    SQLALCHEMY_DATABASE_URI : str
        Make SQLAlchemy to use an in-memory SQLite database during the tests,
        so this way we are not writing dummy test data to our production
        database.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path


class BeforeFirstRequest(TestCase):
    """Testing the functions inside the initialisation file of the ``main``
    package.

    We are testing those decorated by ``before_app_first_request``.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
        os.unlink(db_path)

    def test_create_db(self):
        create_db()
        tester = os.path.exists("test.db")
        self.assertTrue(tester, "The database file can not be found.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
