"""Contains tests pertaining to the creation, deletion and editing of pages.

To run this particular test file use the following command line:

nose2 -v app.tests.pages.tests_routes
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import dummy_post, posting


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
    """Functional tests for the routes found inside the ``pages`` blueprint.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post(title="published page",
                   slug="published_page",
                   is_page=True)

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        """Functional test to verify that our /index routes can list pages.

        The test will see that both published and draft widgets are being
        listed on the page.
        """
        dummy_post(title="draft page", slug="draft_page", is_page=True,
                   is_published=False)
        response = self.tester.get("/pages")
        for title in [b"draft page", b"published page"]:
            self.assertIn(title, response.data,
                          "Did not find the expected pages listed at the "
                          "address.")

    def test_create_page(self):
        """Functional test to verify that we can create a new page.

        Starting from the ``/create_page`` route just like a user would.
        """
        with self.app.test_client() as tester:
            response = posting(tester, '/create_page', is_page=True)
            self.assertIn(b'Page is now live.', response.data,
                          "No message telling you your page went live.")

    def test_edit_page(self):
        """Functional test to verify that we can edit an existing page.

        Starting from the ``<slug>/edit_page`` route just like a user would.
        """
        with self.app.test_client() as tester:
            posting(tester, '/published_page/edit_page',
                    title_field="modified page title")
        response = self.tester.get('/published_page')
        self.assertIn(b'modified page title', response.data,
                      "No message telling you your page was successfully "
                      "edited.")

    def test_delete_page(self):
        """Functional test to verify that we can delete an existing page.

        Starting from the ``<slug>/delete_page`` route just like a user would.
        """
        with self.app.test_client() as tester:
            response = tester.post('/published_page/delete_page',
                                   follow_redirects=True)
            self.assertIn(b'Page deleted', response.data,
                          "No message telling you your dummy page "
                          "was deleted.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
