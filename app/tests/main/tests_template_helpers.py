"""Will test the template filters and globals loaded from the ``main``
 blueprint.

To run this particular test file use the following command line:

nose2 -v app.tests.main.tests_template_helpers
"""

from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import dummy_post, add_social
from app.main.template_helpers import (draft_exists, read_more,
                                       remove_read_more, get_socials)


class TestConfig(Config):
    """ Custom configuration for our tests.

    Attributes
    ----------
    TESTING : bool
        Enable testing mode. Exceptions are propagated rather than handled by
        the app’s error handlers.

        Must be set to True to prevent the mail logger from sending email
        warnings.
    WHOOSHEE_MEMORY_STORAGE : bool
        When set to True use the memory as storage. We need that during our
        tests so the data that we write in the in-memory SQLite database do
        not become indexed.
    SQLALCHEMY_DATABASE_URI : str
        Make SQLAlchemy to use an in-memory SQLite database during the tests,
        so this way we are not writing dummy test data to our production
        database.
    """
    TESTING = True
    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TemplateFilters(TestCase):
    """Contains the tests for our custom template filters.
    """
    with_read_more_tag = "First line.[read_more] Second line."
    without_read_more_tag = "First line. Second line."

    def test_read_more(self):
        """Testing of the ``read_more`` function.
        """
        self.assertEqual("First line.Anchor text.",
                         read_more(self.with_read_more_tag, 'Anchor text.'),
                         "Troncature did not happen as expected for the"
                         " test string.")
        self.assertEqual(self.without_read_more_tag,
                         read_more(self.without_read_more_tag, 'Anchor text.'),
                         "Text was not supposed to be truncated but what is"
                         " returned differ from the test string.")

    def test_remove_read_more(self):
        """Testing of the ``remove_read_more`` function.
        """
        self.assertEqual(self.without_read_more_tag,
                         remove_read_more(self.with_read_more_tag),
                         "Troncature did not happen as expected for the"
                         " test string.")


class TemplateGlobal(TestCase):
    """Contains the tests for our custom template globals.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_draft_exists(self):
        dummy_post(slug='draft_post', is_published=False)
        de = draft_exists()
        self.assertTrue(de, "Function have not been capable to find any draft")

    def test_get_socials(self):
        socials = {'Twitter': 'https://twitter.com/nytimes',
                   'Youtube': 'https://www.youtube.com/user/liveset'}
        add_social('Twitter', 'https://twitter.com/nytimes')
        add_social('Youtube', 'https://www.youtube.com/user/liveset')
        gs = get_socials()
        self.assertEqual(gs, socials, "Links to social websites can not be"
                                      " retrieved.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
