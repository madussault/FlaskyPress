"""Contains tests for the functions found in ``pages/templates_helpers.py``

To run this particular test file use the following command line:

nose2 -v app.tests.pages.tests_template_helpers
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.pages.template_helpers import page_exists, published_pages
from app.tests.utils import dummy_post


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


class TemplateHelpers(TestCase):
    """Testing the decorated functions found in the ``template_helpers``
    module.

    The functions tested are decorated by ``app_template_global`` or
    ``app_context_processor``.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.post = dummy_post(is_page=True)

    def tearDown(self):
        self.app_context.pop()

    def test_page_exists(self):
        pe = page_exists()
        self.assertEqual(self.post, pe, "Function did not return the page "
                                        "object we were looking for.")

    def test_published_pages(self):
        pp = published_pages()
        self.assertIn(self.post, pp["published_pages"],
                      "Function did not return the dictionary we were "
                      "looking for.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
