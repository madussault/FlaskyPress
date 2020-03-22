"""Testing the functions inside the initialisation file of the ``controls``
package.

To run this particular test file use the following command line:

nose2 -v app.tests.controls.tests_init
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.models import (SearchBarControls, CategoriesControls, WidgetOrder,
                        Social)
from app.controls import (default_search_bar_placement, default_socials,
                          default_categories_presence)
from app.tests.utils import control_search_bar, control_categories
from app.controls.dicts import socials


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


class BeforeFirstRequest(TestCase):
    """Testing the functions inside the initialisation file of the ``controls``
    package.

    They are all decorated by ``before_app_first_request``.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_default_search_bar_placement(self):
        default_search_bar_placement()
        query = SearchBarControls.query.first()
        self.assertEqual(query.placement, "navbar",
                         "Function did not write the expected search bar"
                         "placement to the database.")
        db.drop_all()
        db.create_all()
        control_search_bar("sidebar")
        default_search_bar_placement()
        query = SearchBarControls.query.first()
        self.assertEqual(query.placement, "sidebar",
                         "Function re-wrote the existing search bar placement"
                         "when it was not supposed to.")

    def test_default_categories_presence(self):
        default_categories_presence()
        query = CategoriesControls.query.first()
        self.assertEqual(query.presence, "sidebar_and_posts",
                         "The value indicating where categories should be "
                         "displayed on the page was not found in the db.")
        query = WidgetOrder.query.filter_by(name="Category Widget").first()
        self.assertEqual(query.position, "1",
                         "Default position in the sidebar was not assigned to "
                         "our widget.")
        db.drop_all()
        db.create_all()
        control_categories("posts_only")
        default_categories_presence()
        query = CategoriesControls.query.first()
        self.assertEqual(query.presence, "posts_only",
                         "Function re-wrote the existing ``Category.presence``"
                         " value when it was not supposed to.")

    def tests_default_socials(self):
        default_socials()
        social_names = []
        for item in socials.items():
            social_names.append(item[1][0])
        social_names.sort()
        query_social_names = []
        query = Social.query.filter_by(address="").all()
        for obj in query:
            query_social_names.append(obj.name)
        query_social_names.sort()
        self.assertEqual(social_names, query_social_names,
                         "Function did not write the expected social entries"
                         "to the db.")


if __name__ == '__main__':
    unittest.main(verbosity=2)

