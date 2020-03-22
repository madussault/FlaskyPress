"""Test the templates associated with the ``main`` blueprint.

To run this particular test file use the following command line:

nose2 -v app.tests.main.tests_templates
"""

from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import (dummy_post, dummy_user, login,
                             dummy_content_widget)
from bs4 import BeautifulSoup


class TestConfig(Config):
    """ Custom configuration for our tests.

    Attributes
    ----------
    TESTING : bool
        Enable testing mode. Exceptions are propagated rather than handled by
        the app’s error handlers.

        Must be set to True to prevent the mail logger from sending email
        warnings.
    WTF_CSRF_ENABLED : bool
        When set to False all CSRF protection are disabled. We have to
        disable that because no CSRF token are generated when executing a POST
        request directly in our test.
    WHOOSHEE_MEMORY_STORAGE : bool
        When set to True use the memory as storage. We need that during our
        tests so the data that we write in the in-memory SQLite database do
        not become indexed.
    SQLALCHEMY_DATABASE_URI : str
        Make SQLAlchemy to use an in-memory SQLite database during the tests,
        so this way we are not writing dummy test data to our production
        database.
    SITE_NAME : str
        We need this value in our tests to verify that it is displayed in our
        pages where it should.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SITE_NAME = 'Test Title'


class BaseTemplate(TestCase):
    """Contains the tests to verify the content of the base.html template.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post()
        dummy_user()

    def tearDown(self):
        self.app_context.pop()

    def test_page_title(self):
        """Will test that we can assign a title to our page in the base
        template.

        This test concerns the block ``title`` tag.
        """
        response = self.tester.get('/')
        self.assertIn(b'Home - Test Title', response.data,
                      "Title has not been assigned to the /index page")

    def test_duplicate_flash_messages(self):
        """Test that only one flash message is being shown at any one time.
        """
        db.drop_all()
        db.create_all()
        # When a user try to reach the /create route without being
        # logged and no registration exist two flash messages will
        # be added to a list. If our code works all right only the last
        # message from that list will be shown.
        response = self.tester.get('/create_post', follow_redirects=True)
        soup = BeautifulSoup(response.data, features="html.parser")
        flash_list = soup.select('.alert-dismissable')
        self.assertEqual(len(flash_list), 1,
                         "More than one flash message were displayed.")


class Navbar(TestCase):
    """Contains tests to verify the content of the navbar.html template.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_user()

    def tearDown(self):
        self.app_context.pop()

    def test_create_post_in_navbar(self):
        """Testing the presence of the /create_post hyperlink.

        Will only be displayed in the navbar to logged in users.
        """
        response = self.tester.get('/')
        self.assertNotIn(b'<a class="nav-link" href="/create_post">Create '
                         b'Post</a>',
                         response.data,
                         "Hyperlink to the /create_post page can still be "
                         "found in the menu")
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'<a class="nav-link" href="/create_post">'
                      b'Create Post</a>', response.data,
                      "Hyperlink to the /create_post page can not be found"
                      " in the menu")

    def test_logout_in_navbar(self):
        """Testing the presence of the /logout page hyperlink.

        Will only be displayed in the navbar to logged in users.
        """
        response = self.tester.get('/')
        self.assertNotIn(b'<a class="nav-link" href="/logout">Logout</a>',
                         response.data,
                         "Hyperlink to the /logout page can still be found"
                         " in the menu")
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'<a class="nav-link" href="/logout">Logout</a>',
                      response.data,
                      "Hyperlink to the /logout page can not be found"
                      " in the menu")

    def test_existing_drafts_in_navbar(self):
        """Testing the presence of the /draft page hyperlink in the navbar.

        It is supposed to show in the navbar for logged in users only. The
        hyperlink can only be displayed when a draft already exist."""
        dummy_post(is_published=False)
        response = self.tester.get('/')
        self.assertNotIn(b'<a class="nav-link" href="/drafts">Drafts</a>',
                         response.data,
                         "Hyperlink to the /drafts page can still be found"
                         " in the menu for non-logged in users.")
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'<a class="nav-link" href="/drafts">Drafts</a>',
                      response.data,
                      "Hyperlink to the /drafts page can not be found"
                      " in the menu for logged-in users.")

    def test_non_existing_drafts_in_navbar(self):
        """Testing that no hyperlink to the /drafts page appear when no drafts
        exists.

        We will do the test for logged in users, because non-logged in users
        are not supposed to see that hyperlink anyway. This hyperlink is
        supposed to be displayed in the navbar."""
        login(self.tester)
        response = self.tester.get('/')
        self.assertNotIn(b'<a class="nav-link" href="/drafts">Drafts</a>',
                         response.data,
                         "Hyperlink to the /drafts page can not be found"
                         " in the navbar")

    def test_pages_dropdown_menu(self):
        """Testing the ``Pages`` dropdown menu in the navbar.

        This menu is only shown to logged in users. The test will verify the
        presence of the menu and the two hyperlinks it should contain:

        - The static ``Create Page`` hyperlink.
        - The dynamic ``Pages Index`` hyperlink. This item only appears when
          at least one page have already been created.
        """
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'<a class="nav-link dropdown-toggle" href="#" '
                      b'id="PagesDropdown" role="button" data-toggle="dropdown"'
                      b' aria-haspopup="true" '
                      b'aria-expanded="false">\n          Pages',
                      response.data,
                      "The ``pages`` dropdown menu can not be found in the "
                      "navbar.")
        self.assertIn(b'<a class="dropdown-item" href="/create_page">'
                      b'Create Page</a>',
                      response.data,
                      "The ``Create Page`` hyperlink can not be found in the"
                      " ``Pages`` dropdown menu in the navbar.")
        self.assertNotIn(b'<a class="dropdown-item" href="/pages">'
                         b'Pages Index</a>',
                         response.data,
                         "The ``Pages Index`` hyperlink can still be found in "
                         "the ``Pages`` dropdown menu in the navbar.")
        dummy_post(is_page=True)
        response = self.tester.get('/')
        self.assertIn(b'<a class="dropdown-item" href="/pages">Pages Index</a>',
                      response.data,
                      "The ``Pages Index`` hyperlink can not be found in the "
                      "``Pages`` dropdown menu in the navbar.")

    def test_content_widgets_dropdown_menu(self):
        """Testing the ``Content Widgets`` dropdown menu in the navbar.

        This menu is only shown to logged in users. The test will verify the
        presence of the menu and the two hyperlinks it should contain:

        - The static ``Create Widget`` hyperlink.
        - The dynamic ``Widgets Index`` hyperlink. This item only appears when
          at least one widget have already been created.
        """
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'<a class="nav-link dropdown-toggle" href="#" '
                      b'id="ContentWidgetsDropdown" role="button" '
                      b'data-toggle="dropdown" aria-haspopup="true" '
                      b'aria-expanded="false">\n          Content Widgets',
                      response.data,
                      "The ``Content Widgets`` dropdown menu can not be found"
                      " in the navbar.")
        self.assertIn(b'<a class="dropdown-item" '
                      b'href="/create_content_widget">Create Widget</a>',
                      response.data,
                      "The ``Create Widget`` hyperlink can not be found in the"
                      " ``Content Widgets`` dropdown menu in the navbar.")
        self.assertNotIn(b'<a class="dropdown-item" '
                         b'href="/content_widgets">Widgets Index</a>',
                         response.data,
                         "The ``Widgets Index`` hyperlink can still be found"
                         " in the ``Content Widgets`` dropdown menu in the"
                         " navbar.")
        dummy_content_widget()
        response = self.tester.get('/')
        self.assertIn(b'<a class="dropdown-item" '
                      b'href="/content_widgets">Widgets Index</a>',
                      response.data,
                      "The ``Widgets Index`` hyperlink can not be found"
                      " in the ``Content Widgets`` dropdown menu in the "
                      "navbar.")

    def test_controls_dropdown_menu(self):
        """Testing the ``Controls`` dropdown menu in the navbar.

        This menu is only shown to logged in users. The test will verify the
        presence of the menu and the four hyperlinks it should contain:

        - The static ``Search Bar`` hyperlink.
        - The static ``Categories`` hyperlink.
        - The static ``Socials`` hyperlink.
        - The dynamic ``Widgets Order`` hyperlink. This item only appears when
          at least two widgets have been assigned to the sidebar.
        """
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'Controls\n        </a>', response.data,
                      "The ``Controls`` dropdown menu can not be found"
                      " in the navbar.")
        self.assertIn(b'<a class="dropdown-item" href="/controls/search_bar">'
                      b'Search Bar</a>', response.data,
                      "The ``Search Bar`` hyperlink can not be found in the"
                      " ``Controls`` dropdown menu in the navbar.")
        self.assertIn(b'<a class="dropdown-item" href="/controls/categories">'
                      b'Categories</a>', response.data,
                      "The ``Categories`` hyperlink can not be found in the"
                      " ``Controls`` dropdown menu in the navbar.")
        self.assertIn(b'<a class="dropdown-item" href="/controls/categories">'
                      b'Categories</a>', response.data,
                      "The ``Categories`` hyperlink can not be found in the"
                      " ``Controls`` dropdown menu in the navbar.")
        self.assertNotIn(b'<a class="dropdown-item" href="/controls/'
                         b'widgets_order">Widgets Order</a>', response.data,
                         "The ``Widgets Order`` hyperlink can still be found"
                         " in the ``Controls`` dropdown menu in the navbar.")
        dmc = dummy_content_widget()
        dmc.add_to_or_remove_from_sidebar()
        dummy_post()
        response = self.tester.get('/')
        self.assertIn(b'<a class="dropdown-item" href="/controls/'
                      b'widgets_order">Widgets Order</a>', response.data,
                      "The ``Widgets Order`` hyperlink can not be found in "
                      "the ``Controls`` dropdown menu in the navbar.")

    def test_brand_in_navbar(self):
        """Testing that the website name is showing in the navbar.
        """
        response = self.tester.get('/')
        self.assertIn(b'<a class="navbar-brand" href="/index">Test Title</a>',
                      response.data,
                      "The hyperlinked website name is not showing"
                      " in the navbar.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
