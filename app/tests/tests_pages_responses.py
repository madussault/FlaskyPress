"""Testing the response for all the pages in our application.

To run this particular test file use the following command line:

nose2 -v app.tests.tests_pages_responses
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import (dummy_post, dummy_user,
                             dummy_content_widget)


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


class PagesResponses(TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post(categories=["birds"])
        dummy_post(is_page=True, slug="dummy_page")
        dummy_content_widget()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        """Testing the /index page response.
        """
        response = self.tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_drafts(self):
        """Testing the /drafts page response.
        """
        response = self.tester.get('/drafts')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """Testing the /register page response.
        """
        response = self.tester.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Testing the /login page response.
        """
        # A user must be created before accessing the 'login' page or the
        # test client will be redirected to the register page.
        dummy_user()
        response = self.tester.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Testing the /logout page response.
        """
        response = self.tester.get('/logout')
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        """Testing the /create_post page response.
        """
        response = self.tester.get('/create_post')
        self.assertEqual(response.status_code, 200)

    def test_post_detail(self):
        """Testing the /<slug> page response.
        """
        response = self.tester.get('/dummy_post')
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        """Testing the /<slug>/edit_post page response.
        """
        response = self.tester.get('/dummy_post/edit_post')
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        """Testing the /<slug>/delete_post page response.
        """
        response = self.tester.get('/dummy_post/delete_post')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        """Testing the /search page response.
        """
        response = self.tester.get('/search?q=dummy')
        self.assertEqual(response.status_code, 200)

    def test_sitemap(self):
        """Testing the /sitemap page response.
        """
        response = self.tester.get('/sitemap')
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        """Testing the /create_page page response.
        """
        response = self.tester.get('/create_page')
        self.assertEqual(response.status_code, 200)

    def test_edit_page(self):
        """Testing the /<slug>/edit_page page response.
        """
        response = self.tester.get('/dummy_page/edit_page')
        self.assertEqual(response.status_code, 200)

    def test_delete_page(self):
        """Testing the /<slug>/delete_page page response.
        """
        response = self.tester.get('/dummy_page/delete_page')
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        """Testing the <slug>/category page response.
        """
        response = self.tester.get('/birds/category')
        self.assertEqual(response.status_code, 200)

    def test_content_widgets(self):
        """Testing the /content_widgets page response.
        """
        response = self.tester.get('/content_widgets')
        self.assertEqual(response.status_code, 200)

    def test_create_content_widget(self):
        """Testing the /create_content_widget page response.
        """
        response = self.tester.get('/create_content_widget')
        self.assertEqual(response.status_code, 200)

    def test_edit_content_widget(self):
        """Testing the <slug>/edit_content_widget page response.
        """
        response = self.tester.get('/dummy_content_widget/edit_content_widget')
        self.assertEqual(response.status_code, 200)

    def test_delete_content_widget(self):
        """Testing the <slug>/delete_content_widget page response.
        """
        response = self.tester.get('/dummy_content_widget/'
                                   'delete_content_widget')
        self.assertEqual(response.status_code, 200)

    def test_search_bar_control(self):
        """Testing the controls/search_bar page response.
        """
        response = self.tester.get('controls/search_bar')
        self.assertEqual(response.status_code, 200)

    def test_categories_control(self):
        """Testing the controls/categories page response.
        """
        response = self.tester.get('/controls/categories')
        self.assertEqual(response.status_code, 200)

    def test_socials_control(self):
        """Testing the controls/socials page response.
        """
        response = self.tester.get('/controls/socials')
        self.assertEqual(response.status_code, 200)

    def test_widgets_order_control(self):
        """Testing the controls/widgets_order page response.
        """
        response = self.tester.get('/controls/widgets_order')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
