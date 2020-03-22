"""Testing of the database models and other functions found in the models.py
module

To run this particular test file use the following command line:

nose2 -v app.tests.tests_models
"""

from app import db, create_app
from unittest import TestCase
import unittest
from app.models import (Post, User, Category, load_user, util_html_content,
                        reorder_widgets, add_to_or_remove_from_sidebar_util,
                        SearchBarControls, CategoriesControls, ContentWidget,
                        WidgetOrder, Social)
from config import Config
from app.tests.utils import (dummy_user, dummy_post,
                             set_widgets_positions_in_sidebar,
                             dict_of_widgets_positions_in_sidebar)


class TestConfig(Config):
    """ Custom configuration for our tests.

    Attributes
    ----------
    SQLALCHEMY_DATABASE_URI : str
        Make SQLAlchemy to use an in-memory SQLite database during the tests,
        so this way we are not writing dummy test data to our production
        database.
    TESTING : bool
        Enable testing mode. Exceptions are propagated rather than handled by
        the app’s error handlers.

        Must be set to True to prevent the mail logger from sending email
        warnings.
    WHOOSHEE_MEMORY_STORAGE : bool
        When set to True use the memory as storage. We need that during our
        tests so the data that we write in the in-memory SQLite database do
        not become indexed.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    WHOOSHEE_MEMORY_STORAGE = True


class Models(TestCase):
    """Contains the tests for all our database models.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_post(self):
        """Testing of the ``Post`` model.
        """
        categories = [Category(name='birds'), Category(name='cats'),
                      Category(name='dogs')]
        post = Post(title='dummy post',
                    content='dummy content',
                    slug='dummy_post',
                    is_page=False,
                    categories=categories,
                    is_published=True)
        db.session.add(post)
        db.session.commit()
        query = Post.query.get(1)
        self.assertEqual(query, post, "Adding post failed.")
        self.assertEqual(query.categories.all(), categories,
                         "No categories were assigned to the post.")

    def test_user(self):
        """Testing of the ``User`` class model.
        """
        user = dummy_user()
        query = User.query.get(1)
        self.assertEqual(query, user, "Adding user failed.")
        self.assertTrue(query.check_password('pass'),
                        "Checking the password failed.")

    def test_category(self):
        """Testing of the ``Category`` class model.
        """
        c = Category(name='test category')
        c.slugify_name()
        db.session.add(c)
        db.session.commit()
        query = Category.query.get(1)
        self.assertEqual(query, c, "Adding new category failed.")
        self.assertEqual(query.slug, 'test_category',
                         "Adding a slug based on the category name failed.")

    def test_search_bar_controls(self):
        """Testing of the ``SearchBarControls`` class model.
        """
        sbc = SearchBarControls(placement='sidebar')
        db.session.add(sbc)
        db.session.commit()
        query = SearchBarControls.query.get(1)
        self.assertEqual(query, sbc, "Configuring search bar placement "
                                     "failed.")

    def test_categories_controls(self):
        """Testing of the ``CategoriesControls`` class model.
        """
        cc = CategoriesControls(presence='sidebar_and_posts')
        db.session.add(cc)
        db.session.commit()
        query = CategoriesControls.query.get(1)
        self.assertEqual(query, cc, "Configuring where are categories "
                                    "displayed on the website failed.")

    def test_content_widget(self):
        """Testing of the ``ContentWidget`` class model and it's methods.
        """
        cw = ContentWidget(title="dummy title",
                           content="dummy content",
                           is_published=True)
        cw.slugify_title()
        cw.add_to_or_remove_from_sidebar()
        db.session.add(cw)
        db.session.commit()
        query = ContentWidget.query.get(1)
        self.assertEqual(query, cw, "Adding new content widget in the db "
                                    "failed.")
        self.assertEqual(query.slug, 'dummy_title',
                         "Content widget has not been added with the right "
                         "slug.")
        wo = WidgetOrder.query.get(1)
        self.assertEqual(wo.name, 'dummy title',
                         "Content widget has not been added to the table of "
                         "the ``WidgetOrder`` model.")
        query.remove_from_sidebar()
        wo = WidgetOrder.query.get(1)
        self.assertIsNone(wo, "Content widget has not been cleared from the "
                              "table of the ``WidgetOrder`` model.")
        query.add_to_or_remove_from_sidebar()
        db.session.commit()
        query.remove_invalid_title_from_sidebar("new title")
        wo = WidgetOrder.query.get(1)
        self.assertIsNone(wo, "Entry for the old name of our content widget "
                              "has not been cleared from the table of the "
                              "``WidgetOrder`` model.")

    def test_social(self):
        """Testing of the ``Social`` class model.
        """
        s = Social(name='Twitter', address='https://twitter.com/dcexaminer')
        db.session.add(s)
        db.session.commit()
        query = Social.query.get(1)
        self.assertEqual(query, s, "Adding social account address to db"
                                   " failed.")

    def test_widget_order(self):
        """Testing of the ``WidgetOrder`` class model.
        """
        wo = WidgetOrder(name='Category Widget', position='1')
        db.session.add(wo)
        db.session.commit()
        query = WidgetOrder.query.get(1)
        self.assertEqual(query, wo, "Adding to db the position of a widget in "
                                    "the sidebar failed.")


class FunctionsOutsideModels(TestCase):
    """Contains tests for all the other functions outside our models.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_load_user(self):
        """Testing that our function to load a user to flask login works.
        """
        user = dummy_user()
        loaded_user = load_user('1')
        self.assertEqual(user, loaded_user, "Adding new category failed.")

    def test_util_html_content(self):
        """Testing of the ``util_html_content`` function.

        Here we will be testing 3 things:
        - That the markdown formatting is converted to html.
        - That media URLs are converted into embeds.
        - That non-media URLs are converted to hyperlinks.
        """
        media = "youtube video: https://www.youtube.com/watch?v=aOC8E8z_ifw"
        general_markdown = "this written in **bold**."
        url_to_hyperlink = "https://www.google.com/"

        p = dummy_post(content=media, slug='media')
        self.assertIn('title="The Mandalorian | Official Trailer |',
                      util_html_content(p),
                      "Html for the embed has not been returned by the"
                      " function.")
        p = dummy_post(content=general_markdown, slug='general_markdown')
        self.assertIn('<strong>bold</strong>',
                      util_html_content(p),
                      "Html for the bold markdown has not been returned by the"
                      " function.")
        p = dummy_post(content=url_to_hyperlink, slug='url_to_hyperlink')
        self.assertIn('<a href="https://www.google.com/">'
                      'https://www.google.com/</a>',
                      util_html_content(p),
                      "Url was not converted to an hyperlink by the function.")

    def test_reorder_widgets(self):
        """Testing of the ``reorder_widgets`` function.

        This function assign a new position to the widgets in the
        ``WidgetOrder`` model.
        """
        widgets_positions = {"widget1": "1", "widget2": "3", "widget3": "4"}
        expected = {'widget1': '1', 'widget2': '2', 'widget3': '3'}
        set_widgets_positions_in_sidebar(widgets_positions)
        reorder_widgets()
        dic_of_query = dict_of_widgets_positions_in_sidebar()
        self.assertEqual(dic_of_query, expected, "Widgets positions failed to"
                                                 " be reordered.")

    def test_add_to_or_remove_from_sidebar(self):
        """Testing of the ``add_to_or_remove_from_sidebar`` function.

        This function assigns a default position to the widgets when they are
        inserted into the sidebar. It also removes a widget from the sidebar
        if it's placement is changed by the user.
        """
        # We will first test that a widget already positioned in the sidebar
        # is ignored by the function.
        widgets_positions = {"widget1": "1",
                             "widget2": "2",
                             "Category Widget": "3"}
        set_widgets_positions_in_sidebar(widgets_positions)
        add_to_or_remove_from_sidebar_util('sidebar_and_posts',
                                           'sidebar_and_posts',
                                           'Category Widget')
        dic_of_query = dict_of_widgets_positions_in_sidebar()
        expected = {'widget1': '1', 'widget2': '2', "Category Widget": "3"}
        self.assertEqual(dic_of_query, expected,
                         "Initial widget order was unexpectedly modified.")
        db.drop_all()
        db.create_all()
        # We will then test that a widget newly inserted into the sidebar
        # is assigned the last position.
        widgets_positions = {"widget1": "1",
                             "widget2": "2"}
        set_widgets_positions_in_sidebar(widgets_positions)
        add_to_or_remove_from_sidebar_util('sidebar_and_posts',
                                           'sidebar_and_posts',
                                           'Category Widget')
        dic_of_query = dict_of_widgets_positions_in_sidebar()
        expected = {'widget1': '1', 'widget2': '2', 'Category Widget': '3'}
        self.assertEqual(dic_of_query, expected,
                         "Widget position is not the right one. The position"
                         " is supposed to be third and last.")
        db.drop_all()
        db.create_all()
        # We will finally test that a widget that is not supposed to be placed
        # in the sidebar stay excluded.
        widgets_positions = {"widget1": "1",
                             "Category Widget": "2",
                             "widget2": "3"}
        set_widgets_positions_in_sidebar(widgets_positions)
        add_to_or_remove_from_sidebar_util('sidebar_and_posts',
                                           'no_categories',
                                           'Category Widget')
        dic_of_query = dict_of_widgets_positions_in_sidebar()
        expected = {'widget1': '1', 'widget2': '2'}
        self.assertEqual(dic_of_query, expected,
                         "Widgets positions are not what is expected.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
