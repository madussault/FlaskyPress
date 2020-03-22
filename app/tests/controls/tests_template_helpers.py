"""Contains tests for the functions found in ``controls/templates_helpers.py``

To run this particular test file use the following command line:

nose2 -v app.tests.controls.tests_template_helpers
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import (dummy_post, control_categories,
                             control_search_bar,
                             add_three_dummy_widget_positions)
from app.models import SearchBarControls, CategoriesControls
from app.controls.template_helpers import (ordered_widgets,
                                           categories_presence,
                                           sidebar_widget_count,
                                           search_bar_placement)


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


class TemplateGlobal(TestCase):
    """Contains tests for the blueprint's custom template global functions.

    These functions can be found in the ``controls/templates_helpers.py``. They
    are decorated with ``app_template_global``.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post()
        control_categories("no_posts")
        control_search_bar('navbar')

    def tearDown(self):
        self.app_context.pop()

    def test_search_bar_placement(self):
        """Testing of the ``search_bar_placement`` function.
        """
        search_bar_placement()
        query = SearchBarControls.query.first()
        self.assertEqual(query.placement, 'navbar',
                         "Function was not capable to get the value "
                         "representing the search bar placement.")

    def test_categories_presence(self):
        categories_presence()
        query = CategoriesControls.query.first()
        self.assertEqual(query.presence, 'no_posts',
                         "Function was not capable to get the value "
                         "representing where the categories can be found on "
                         "the page.")

    def test_sidebar_widget_count(self):
        add_three_dummy_widget_positions()

        self.assertEqual(sidebar_widget_count(), 3,
                         "Total number of entry in the the table of the"
                         " ``WidgetOrder`` is not what is expected.")

    def test_ordered_widgets(self):
        add_three_dummy_widget_positions()
        ow = ordered_widgets()
        expected = ['Search Bar Widget', 'Category Widget',
                    'Dummy Content Widget']
        self.assertEqual(expected, ow, "List of widgets name was not returned"
                                       "with the expected order.")


if __name__ == '__main__':
    unittest.main(verbosity=2)