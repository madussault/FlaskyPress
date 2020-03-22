"""Contains tests to verify that our blueprints register using url prefixes.

To run this particular test file use the following command line:

nose2 -v app.tests.tests_url_prefix
"""

from app import db, create_app
import unittest
from unittest import TestCase
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
    SQLALCHEMY_DATABASE_URI : str
        Make SQLAlchemy to use an in-memory SQLite database during the tests,
        so this way we are not writing dummy test data to our production
        database.
    URL_PREFIX : str
        Our routes will be accessible starting from the subdirectory
        named by that string.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    URL_PREFIX = '/test'


class UrlPrefix(TestCase):
    """Contains tests to verify that our app can be served from a domain
    subdirectory.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_prefixed_url(self):
        """Testing the /index page response when it's url is prefixed.
        """
        response = self.tester.get('/test', follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                         "We can't access the `/index` route when we try to do"
                         " so starting from the testing prefix.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
