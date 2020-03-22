"""Contains unit tests for the functions inside the /controls/form.py module.

To run this particular test file use the following command line:

nose2 -v app.tests.controls.tests_forms
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import dummy_post
from app.models import SearchBarControls
from app.controls.forms import position_choices, prevent_identical
from app.controls import default_categories_presence
from wtforms.validators import ValidationError


class TestConfig(Config):
    """ Custom configuration for our tests.

    Attributes
    ----------
    TESTING : bool
        Enable testing mode. Exceptions are propagated rather than handled by
        the app’s error handlers.

        Must be set to True to prevent the mail logger from sending email
        warnings.
    LOGIN_DISABLED : bool
        When set to True the /routes protected by Flask-login become
        accessible without having to log into the app.
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
    LOGIN_DISABLED = True
    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class Forms(TestCase):
    """Testing the functions found inside the forms of the ``controls``
    blueprint.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post(categories=["birds"])
        default_categories_presence()
        sbc = SearchBarControls(placement="sidebar")
        sbc.add_to_or_remove_from_sidebar()
        db.session.add(sbc)
        db.session.commit()

    def tearDown(self):
        self.app_context.pop()

    def test_position_choices(self):
        choices = position_choices()
        expected = [('1', '1'), ('2', '2')]
        self.assertEqual(expected, choices,
                         "Function did not return the right tuples of "
                         "(value, label) pairs.")

    def test_prevent_identical(self):
        # For this test we first need to make a mock form and field objects
        # that we are going to pass to the function.
        class MockForm:
            data = "mock data"
            name = "mock name"

        class MockField:
            data = "mock data"
            name = "mock different name"
        # Then we can proceed with the tests.
        with self.assertRaises(ValidationError,
                               msg="Identical choices were not detected by "
                                   "the function."):
            prevent_identical([MockForm()], MockField())

        class MockField:
            data = "mock different data"
            name = "mock different name"
        try:
            prevent_identical([MockForm()], MockField())
        except ValidationError:
            self.fail("Function failed to validate the input.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
