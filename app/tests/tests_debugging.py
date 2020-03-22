"""Testing of the functions contained in the debugging.py module.

Two functions are being tested by this test file. One send an email alerting
the admin when the application crash. The other write logging output to a
file on disk.

To run this particular test file use the following command line:

nose2 -v app.tests.tests_debugging
"""

from app import create_app
import unittest
from unittest import TestCase
from config import Config


class TestConfig(Config):
    """ Custom configuration for our tests.

    Attributes
    ----------
    DEBUG : bool
        Enable debug mode. Need to be set to false for the mail logger and the
        rotating file handler to work. Those logging extensions are usually
        only used in production environment when DEBUG is set to false and
        could be inconvenient to use during the development phase, a time where
        debug is often set to TRUE.
    """
    DEBUG = False


class Debugging(TestCase):
    """Contains tests for the mail logger and the log-to-file functionality.
    """
    def setUp(self):
        self.app = create_app(TestConfig)

    def test_mail_logger(self):
        """Will test the implementation of our mail logger.

        Here we want to make sure that are our mail handler is being added to
        the logger and is configured to send an email on warning.
        """
        tester = str(self.app.logger.handlers)
        self.assertIn('<SMTPHandler (ERROR)>', tester,
                      'The mail handler was not added to the logger or is '
                      'not configured with the right logging level.')

    def test_logging_to_file(self):
        """Will test the implementation of our file handler.

        Here we're making sure that our rotating file handler is being added
        to the logger and is configured to write the log to file at the INFO
        level.
        """
        tester = str(self.app.logger.handlers)
        self.assertIn('RotatingFileHandler', tester,
                      'The rotating file handler used to write the log to file'
                      ' was not added to the logger.')
        self.assertIn('(INFO)', tester, 'The rotating file handler was not '
                                        'set at the INFO level.')


if __name__ == '__main__':
    unittest.main(verbosity=2)

