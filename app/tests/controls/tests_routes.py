"""Testing the different configuration functionality of our app.

The functionality tested are those found inside the ``controls`` blueprint.

To run this particular test file use the following command line:

nose2 -v app.tests.controls.tests_routes
"""
from app import db, create_app
import unittest
from unittest import TestCase
from config import Config
from bs4 import BeautifulSoup
from app.tests.utils import dummy_post


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
    """Functional tests for the routes found inside the ``controls`` blueprint.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.category = "birds"
        dummy_post(categories=[self.category])

    def tearDown(self):
        self.app_context.pop()

    def util_test_search_bar_control(self, choice, markup):
        """Will return where and if our search bar is displayed on the page.

        paramaters
        ----------
        choice : str
            Indicate where and if our search bar should be displayed.

        markup : str
            Part included in the html of the search bar we're looking for.

        return
        ------
        soup.select(markup) : list
            Contains the name of the place where the search bar can be found
            on the page.
        """
        with self.app.test_client() as tester:
            tester.post('/controls/search_bar',
                        data={'placement_field': choice})
        response = self.tester.get('/')
        soup = BeautifulSoup(response.data, "html.parser")
        return soup.select(markup)

    def test_search_bar_control(self):
        """Testing that we can control where and if our search bar is
        displayed.
        """
        markup = 'nav input[placeholder="Search for..."]'
        in_navbar = self.util_test_search_bar_control('navbar', markup)
        self.assertTrue(in_navbar,
                        "Search bar could not be found in the navbar.")
        markup = '.col-md-4 input[placeholder="Search for..."]'
        in_sidebar = self.util_test_search_bar_control('sidebar', markup)
        self.assertTrue(in_sidebar,
                        "Search bar could not be found in the sidebar.")
        markup = 'input[placeholder="Search for..."]'
        no_search = self.util_test_search_bar_control('no_search', markup)
        self.assertFalse(no_search,
                        "Search bar could still be found on the page")

    def util_test_categories_control(self, choice):
        """Will return where and if our categories are displayed on the page.

        paramaters
        ----------
        choice : str
            This string indicate where and if our categories should be
            displayed.

        return
        ------
        places_found : list
            Name the places where the category can be found on the page.
        """
        places_found = []
        with self.app.test_client() as tester:
            tester.post('/controls/categories',
                        data={'presence_field': choice})
        response = self.tester.get('/')
        soup = BeautifulSoup(response.data, "html.parser")
        in_post = f'.d-inline a[href="/{self.category}/category"]'
        in_sidebar = f'.card a[href="/{self.category}/category"]'
        if soup.select(in_post):
            places_found.append("in post")
        if soup.select(in_sidebar):
            places_found.append("in sidebar")
        return places_found

    def test_categories_control(self):
        """Testing that we can control where and if our our categories are
        displayed.
        """
        places_found = self.util_test_categories_control("posts_only")
        self.assertEqual(places_found, ["in post"],
                         "Category is not where it should be on the page.")
        places_found = self.util_test_categories_control("sidebar_and_posts")
        self.assertEqual(places_found, ["in post", "in sidebar"],
                         "Category could not be found in the post or the "
                         "sidebar.")
        places_found = self.util_test_categories_control("no_categories")
        self.assertEqual(places_found, [],
                         "Category can still be found on the page.")

    def test_socials_control(self):
        """Testing that we can add our social addresses in the footer.
        """
        with self.app.test_client() as tester:
            tester.post('/controls/socials',
                        data={'twitter_address': 'https://twitter.com/nytimes'})
        response = self.tester.get('/')
        self.assertIn(b'https://twitter.com/nytimes', response.data,
                      "Social address could not be found on the page.")

    def util_test_widgets_order_control(self):
        """Returns the order of the widgets in the sidebar.

        return
        ------
        widgets_order : list
            List of strings each identifying a type a widget. Their order is
            the list represent the one they were assigned in the sidebar.
        """
        response = self.tester.get('/')
        soup = BeautifulSoup(response.data, "html.parser")
        widgets_header = soup.select(".card-header")
        widgets_order = []
        for widget_header in widgets_header:
            if "Dummy Content Widget" in widget_header:
                widgets_order.append("content widget")
            if "Categories" in widget_header:
                widgets_order.append("categories")
        return widgets_order

    def test_widgets_order_control(self):
        """Testing that we are capable to reorder the widgets in the sidebar.
        """
        with self.app.test_client() as tester:
            tester.post("/create_content_widget", data={
                'title_field': "Dummy Content Widget",
                'content_field': "test content",
                'publish': 1},
                                   follow_redirects=True)
        widgets_order = self.util_test_widgets_order_control()
        self.assertEqual(widgets_order, ["categories", "content widget"],
                         "Initial order of the widgets in the sidebar is not "
                         "right.")
        with self.app.test_client() as tester:
            tester.post("/controls/widgets_order", data={
                'dummy_content_widget': "1",
                'category_widget': "2"})
        widgets_order = self.util_test_widgets_order_control()
        self.assertEqual(widgets_order, ["content widget", "categories"],
                         "Reordering of the widgets in the sidebar did not"
                         "work as expected.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
