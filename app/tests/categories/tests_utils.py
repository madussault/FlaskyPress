"""Testing the code found in the ``categories/utils`` module.

To run this particular test file use the following command line:

nose2 -v app.tests.categories.tests_utils
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.categories.utils import set_categories
from app.tests.utils import add_category
from app.models import Category


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


class Utils(TestCase):
    """Contains tests for the utility functions of the ``categories``
     blueprint.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_set_categories(self):
        # First we will test that our function is capable to create a new
        # category object from a new category name (name can't be found in the
        # table of the ``Category`` table.).
        expected = Category(name="cat")
        tested_func = set_categories(["cat"])
        self.assertEqual(expected.name, tested_func[0].name,
                         "Function did not return the Category object we were "
                         "looking for.")
        # Then we will test that if a new post is saved under an existing
        # category, it is this category that is being attached to the post
        # instead of creating a category with the same name.
        expected = add_category("birds")
        tested_func = set_categories(["birds"])
        self.assertEqual(expected, tested_func[0],
                         "Function did not return the Category object we were "
                         "looking for.")
        # Then will test that an empty string and the "uncategorized" string
        # are being ignored by the function.
        tested_func = set_categories(["", "uncategorized"])
        self.assertEqual([], tested_func,
                         "Function did not return an empty list.")


if __name__ == '__main__':
    unittest.main(verbosity=2)