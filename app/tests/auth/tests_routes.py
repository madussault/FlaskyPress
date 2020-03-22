"""Testing the authentication process of the app.

Which comprises the registration, login and logout functionality.

To run this particular test file use the following command line:

nose2 -v app.tests.auth.tests_routes
"""
from flask import request, url_for
from app import db, create_app
from unittest import TestCase
import unittest
from config import Config
from app.tests.utils import dummy_user, login


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
    SQLALCHEMY_DATABASE_URI : str
        Make SQLAlchemy to use an in-memory SQLite database during the tests,
        so this way we are not writing dummy test data to our production
        database.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class Registration(TestCase):
    """Contains the tests pertaining to the registration functionality of our
    app.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        self.app_context.pop()

    def test_registration_successful(self):
        """Will test that we can successfully register a new user.

        Testing of the whole registration process starting from the
        /register page.
        """
        with self.app.test_client() as tester:
            response = tester.post('/register',
                                   data=dict(pass_field1='test_pass',
                                             pass_field2='test_pass'),
                                   follow_redirects=True)
            self.assertIn(b'You are now registered', response.data,
                          "Registration failed.")
            self.assertEqual(request.path, url_for('auth.login'),
                             "Redirect to the /login page after registration "
                             "failed.")

    def test_someone_is_already_registered(self):
        """Testing that only one user can register as the admin.

        Will test that we are redirected away from the /register page if a
        registration already exist.
        """
        dummy_user()
        with self.app.test_client() as tester:
            response = tester.get('/register', follow_redirects=True)
            self.assertIn(b'Someone has already registered', response.data,
                          "Content of the response doesn't tell you that a "
                          "registration already occurred.")
            self.assertEqual(request.path, url_for('main.index'),
                             "Redirect to the /index page failed.")

    def test_not_registered(self):
        """Test that the /login page can only be accessed if a user
         is registered.
        """
        with self.app.test_client() as tester:
            response = tester.get('/login', follow_redirects=True)
            self.assertIn(b'You need to register', response.data,
                          "No message telling you you you need to register")
            self.assertEqual(request.path, url_for('auth.register'),
                             "Redirect to the /register page failed.")


class LoginLogout(TestCase):
    """Contains the tests pertaining to the login and logout functionality of
    our app.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            dummy_user()

    def test_successful_login(self):
        """Test that a user can log into the app after inputting the right
        password.
        """
        with self.app.test_client() as tester:
            response = login(tester)
            self.assertEqual(request.path, url_for('main.index'),
                             "Redirect to the /index page failed.")
            self.assertIn(b'You are now logged', response.data,
                          "Login failed.")

    def test_failed_login(self):
        """Testing that a user is blocked from login in using an invalid
        password.
        """
        response = login(self.tester, password="wrong_pass")
        self.assertIn(b'Incorrect password', response.data,
                      "No message telling you you entered a wrong password.")

    def test_already_logged_in(self):
        """Test that a user already logged in is redirected away from the
         /login page.
        """
        with self.app.test_client() as tester:
            login(tester)
            response = tester.get('/login', follow_redirects=True)
            self.assertEqual(request.path, url_for('main.index'),
                             "Redirect to the /index page failed.")
            self.assertIn(b'You are already logged in', response.data,
                          "No message telling you you are already logged in.")

    def test_login_required_denied(self):
        """Test that a non logged in user can not access protected routes.

        Protection comes from the ``login_required`` decorator. When a
        non-logged in user try to access a protected page he is redirected
        to the /login page.
        """
        with self.app.test_client() as tester:
            # A non-logged in user can not access the /create_post route.
            response = tester.get('/create_post', follow_redirects=True)
            self.assertEqual(request.path, url_for('auth.login'),
                             "Redirect to the /login page failed.")
            self.assertIn(b'Please log in to access this page.', response.data,
                          "No message telling you you have to log in to access"
                          " the page.")

    def test_login_required_accepted(self):
        """Testing that a logged in user can access protected routes.

        Protection comes from the ``login_required`` decorator.
        """
        # A logged in user can access the /create_post route.
        login(self.tester)
        response = self.tester.get('/create_post')
        self.assertIn(b'New Post', response.data,
                      "You failed to access a page protected "
                      "by ``login_required``.")

    def test_remember_me(self):
        """Testing that the ``remember me`` checkbox can extend our session
        duration.
        """
        with self.app.test_client() as tester:
            login(tester)
            self.assertIn("remember_token", request.cookies,
                          "remember_me cookie can't be found.")

    def test_logout(self):
        """Test that we can effectively log out of our application.
        """
        with self.app.test_client() as tester:
            login(tester)
            tester.post('/logout', follow_redirects=True)
            self.assertEqual(request.path, url_for('auth.login'),
                             "Redirect to the /login page did not happen "
                             "after attempting to logout.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
