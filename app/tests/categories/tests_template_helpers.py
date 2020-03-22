"""Testing the code found in the ``categories/template_helpers`` module.

To run this particular test file use the following command line:

nose2 -v app.tests.categories.tests_template_helpers
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import dummy_post
from app.categories.template_helpers import categories_w_post_count


class TestConfig(Config):
    """Custom configuration for our tests.

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


class AppTemplateGlobal(TestCase):
    """Contains tests for the functions that will be made available in all
    templates.

    These functions are decorated by ``@bp.app_template_global()``.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_categories_w_post_count(self):
        dummy_post(categories=["birds", "dogs"], slug="post_1")
        dummy_post(categories=["birds"], slug="post_2")
        dic = categories_w_post_count()
        self.assertEqual(dic["birds"], 2,
                         "Total number of posts posted under our dummy "
                         "category is not what is expected")


if __name__ == '__main__':
    unittest.main(verbosity=2)
