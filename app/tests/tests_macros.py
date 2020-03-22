"""Contains tests for all the macros of the application.

To run this particular test file use the following command line:

nose2 -v app.tests.tests_macros
"""

from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from app.tests.utils import (dummy_post, dummy_user, login, posting,
                             add_social)
from bs4 import BeautifulSoup
from app.models import CategoriesControls


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
    LOGIN_DISABLED : bool
        When set to True the /routes protected by Flask-login become
        accessible without having to log into the app.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    LOGIN_DISABLED = True


class Macros(TestCase):
    """Contains tests for all the macros of the application.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post()
        dummy_post(is_published=False, slug='draft_dummy_post')
        dummy_user()
        add_social('Twitter', 'https://twitter.com/nytimes')

    def tearDown(self):
        self.app_context.pop()

    def test_post_url(self):
        """Testing the ``post_url`` macro.
        """
        self.app.config['LOGIN_DISABLED'] = False
        response = self.tester.get('/')
        self.assertIn(b'<a href="/dummy_post">Dummy post</a>', response.data,
                      "Title of the post on the /index page is not leading "
                      "to the post detail for anonymous users.")
        login(self.tester)
        response = self.tester.get('/')
        self.assertIn(b'<a href="/dummy_post/edit_post">Dummy post</a>',
                      response.data,
                      "Title of the post on the /index page is not leading "
                      "to the post edit page for logged-in users.")
        response = self.tester.get('/drafts')
        self.assertIn(b'<a href="/draft_dummy_post/edit_post">Dummy post</a>',
                      response.data,
                      "Title of the post on the /drafts page is not leading "
                      "to the post edit page.")

    def test_set_title(self):
        """Testing the ``set_title`` macro.
        """
        response = self.tester.get('/')
        self.assertIn(b'Latest Posts', response.data,
                      "Title of the /index page is not what is expected.")
        response = self.tester.get('/search?q=test')
        self.assertIn(b'Search Results', response.data,
                      "Title of the /search page is not what is expected.")
        response = self.tester.get('/uncategorized/category')
        self.assertIn(b'Category: uncategorized', response.data,
                      "Title of the /category page is not what is expected.")
        response = self.tester.get('/drafts')
        self.assertIn(b'Latest Drafts', response.data,
                      "Title of the /drafts page is not what is expected.")

    def test_render_categories(self):
        """Testing the ``render_categories`` macro.
        """
        # We will first test the preview of a post and a published post
        # posted under a single category.
        response = posting(self.tester, '/create_post', preview='Preview',
                           title_field='single_category',
                           categories_field_0='cats')
        self.assertIn(b'\n\nin\n\n\n\n\ncats.', response.data,
                      "Category is not displayed in the right manner when "
                      "previewing a post with single category.")
        response = posting(self.tester, '/create_post',
                           title_field='single_category',
                           categories_field_0='cats')
        self.assertIn(b'\n\nin\n\n\n\n\n<a href="/cats/category">cats.</a>',
                      response.data,
                      "Hyperlinked category is not displayed in the right "
                      "manner for a published post with a single category.")
        # We will do the same thing now but for a post with two categories
        response = posting(self.tester, '/create_post', preview='Preview',
                           title_field='two_category',
                           categories_field_0='dogs',
                           categories_field_1='birds')
        self.assertTrue(b'\n\nin\n\n\n\n\ndogs,\n\n\n\n\n\nbirds.'
                        in response.data or
                        b'\n\nin\n\n\n\n\nbirds,\n\n\n\n\n\ndogs.'
                        in response.data,
                        "Categories are not displayed in the right manner"
                        " when previewing a post with two categories.")
        response = posting(self.tester, '/create_post',
                           title_field='two_category',
                           categories_field_0='dogs',
                           categories_field_1='birds')
        self.assertTrue(b'\n\nin\n\n\n\n\n<a href="/dogs/category">dogs,'
                        b'</a>\n\n\n\n\n\n<a href="/birds/category">birds.</a>'
                        in response.data or
                        b'\n\nin\n\n\n\n\n<a href="/birds/category">birds,'
                        b'</a>\n\n\n\n\n\n<a href="/dogs/category">dogs.</a>'
                        in response.data,
                        "Hyperlinked categories are not displayed in the"
                        " right manner for a published post with two "
                        "categories.")
        # Then we test a post with no category.
        response = posting(self.tester, '/create_post', preview='Preview',
                           title_field='no_category')
        self.assertIn(b'\n\nin\n\n\nuncategorized.', response.data,
                      "No tag with the word `uncategorized` can be found when"
                      " previewing a post without categories.")
        response = posting(self.tester, '/create_post',
                           title_field='no_category')
        self.assertIn(b'\n\nin\n\n\n<a href="/uncategorized/category">'
                      b'uncategorized.</a>', response.data,
                      "No tag with the hyperlinked word `uncategorized` can"
                      " be found for a post published without categories.")
        # Finally we will test a post when categories have been configured to
        # not show up anywhere on the site.
        cg = CategoriesControls.query.first()
        cg.presence = 'no_categories'
        db.session.commit()
        response = posting(self.tester, '/create_post', title_field='single_category',
                categories_field_0='cats')
        self.assertNotIn(b'cats', response.data,
                         "A category can still be found in our post after "
                         "the category functionality have been disabled "
                         "site wide.")

    def test_social_icon(self):
        """Testing the ``social_icon`` macro.
        """
        response = self.tester.get('/')
        soup = BeautifulSoup(response.data, features="html.parser")
        svg_elem = soup.select('footer svg')
        svg_width = svg_elem[0].get('width')
        self.assertEqual('48', svg_width,
                         "Width for the social icon in the footer is wrong.")
        response = self.tester.get('/controls/socials')
        soup = BeautifulSoup(response.data, features="html.parser")
        svg_elem = soup.select('form svg')
        svg_width = svg_elem[0].get('width')
        self.assertEqual('32', svg_width,
                         "Width for the social icon in the `/controls/socials`"
                         " page is wrong.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
