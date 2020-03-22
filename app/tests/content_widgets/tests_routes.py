"""Contains tests pertaining to the creation, deletion and editing of content
widgets.

To run this particular test file use the following command line:

nose2 -v app.tests.content_widgets.tests_routes
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import dummy_content_widget
from app.models import ContentWidget


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
    WTF_CSRF_ENABLED : bool
        When set to False all CSRF protection are disabled. We have to
        disable that because no CSRF token are generated when executing a POST
        request directly in our test.
    """
    TESTING = True
    LOGIN_DISABLED = True
    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class Routes(TestCase):
    """Functional tests for the routes found inside the ``categories``
    blueprint.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_content_widget()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        """Functional test to verify that our /index routes can list content
         widgets.

        The test will see that both published and draft widgets are being
        listed on the page.
        """
        dummy_content_widget(title="draft content widget",
                             slug="draft_content_widget", is_published=False)
        response = self.tester.get("/content_widgets")
        for title in [b"draft content widget", b"Dummy Content Widget"]:
            self.assertIn(title, response.data,
                          "Did not find the expected content widgets listed"
                          "on the page.")

    def test_create_content_widget(self):
        """Functional test to verify that we can create a content widget.

        Starting from the ``/create_content_widget`` route just like a user
        would.
        """
        with self.app.test_client() as tester:
            response = tester.post("/create_content_widget", data={
                'title_field': "dummy content widget",
                'content_field': "test content",
                'publish': 1},
                            follow_redirects=True)
            self.assertIn(b"dummy content widget",
                          response.data,
                          "Failed to create a new content widget.")

    def test_edit_content_widget(self):
        """Functional test to verify that we can edit a content widget.

        Starting from the ``<slug>/delete_content_widget`` route just like a
        user would.
        """
        with self.app.test_client() as tester:
            response = tester.post("/dummy_content_widget/edit_content_widget",
                                   data={
                                       'title_field': "edited content widget",
                                       'publish': 1},
                                   follow_redirects=True)
            self.assertIn(b"edited content widget",
                          response.data,
                          "Failed to edit your dummy content widget.")

    def test_delete_content_widget(self):
        """Functional test to verify that we can delete a content widget.

        Starting from the ``/edit_content_widget`` route just like a user
        would.
        """
        with self.app.test_client() as tester:
            tester.post("/dummy_content_widget/delete_content_widget",
                        follow_redirects=True)
        cw = ContentWidget.query.first()
        self.assertIsNone(cw, "Dummy content widget was not removed from the "
                              "database.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
