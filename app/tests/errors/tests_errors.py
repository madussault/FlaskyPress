"""Test the routes contained in the errors/handlers.py module

To run this particular test file use the following command line:

nose2 -v app.tests.errors.tests_errors
"""

from app import create_app, db
import unittest
from unittest import TestCase
from config import Config


class TestConfig(Config):
    """ Custom configuration for our tests.

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
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class Error(TestCase):
    """Contains test related to the handling of http errors.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_error_404(self):
        """Will test that 404 errors returns a specific template.

        This template is a custom one and is being served by a route
        implemented to specifically handle the 404 errors.
        """
        response = self.tester.get('/random_string')
        self.assertEqual(response.status_code, 404,
                         "Reaching the non-existent page doesn't return"
                         " a 404 error.")
        self.assertIn(b'File Not Found', response.data,
                      "Content of the response doesn't match the /404 page.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
