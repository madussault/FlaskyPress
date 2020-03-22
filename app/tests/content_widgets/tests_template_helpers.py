"""Testing the functions found in the ``categories/template_helpers`` module.

To run this particular test file use the following command line:

nose2 -v app.tests.content_widgets.tests_template_helpers
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.content_widgets.template_helpers import (content_widget_exists,
                                                  get_content_widget)
from app.tests.utils import dummy_content_widget


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
    ``app_template_filter``.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.dcw = dummy_content_widget()

    def tearDown(self):
        self.app_context.pop()

    def test_content_widget_exists(self):
        cwe = content_widget_exists()
        self.assertEqual(self.dcw, cwe, "Function did not return the content "
                                        "widget object we were looking for")

    def test_get_content_widget(self):
        gcw = get_content_widget("Dummy Content Widget")
        self.assertEqual(self.dcw, gcw, "Function did not return the content "
                                        "widget object we were looking for")


if __name__ == '__main__':
    unittest.main(verbosity=2)
