"""Testing the functionality served by the routes of the ``main`` blueprint.

To run this particular test file use the following command line:

nose2 -v app.tests.main.tests_routes
"""
from flask import request, url_for
from app import db, create_app
from unittest import TestCase
import unittest
from config import Config
from app.tests.utils import dummy_post, posting
from app.models import Post
from datetime import datetime


class TestConfig(Config):
    """Custom configuration for our tests.

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
    POSTS_PER_PAGE : int
        Set the maximum number of post per page. A small number will suffice
        for our tests.
    """
    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    WHOOSHEE_MEMORY_STORAGE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    POSTS_PER_PAGE = 2


class Pagination(TestCase):
    """Contains tests for the pagination in our routes.

    Routes concerned:
    - /index
    - /drafts
    - /search

    Pagination tests also test that our posts are being displayed by order of
    date, from the most recent to the oldest. If the oldest post is the one
    found on the second page it means that it was ordered last and that it was
    also effectively classified as the oldest post.
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

    def test_pagination_for_index(self):
        """Will test pagination for our /index route.
        """
        # We will add several dummy posts so we can create at least
        # one more page to paginate too when reaching the /index route.
        # The same pattern of creating dummy posts is going to be used for
        # the subsequent tests.
        dummy_post(title='Dummy post1', slug="dummy_post1",
                   is_published=True)
        dummy_post(title='Dummy post2', slug="dummy_post2",
                   is_published=True)
        dummy_post(title='Dummy post3', slug="dummy_post3",
                   is_published=True)
        response = self.tester.get('/index?page=2')
        self.assertIn(b'Dummy post1', response.data,
                      "Can't find the last dummy post on the second page of "
                      "the /index.")

    def test_pagination_for_drafts(self):
        """Will test pagination for our /drafts route.
        """
        dummy_post(title='Dummy post1', slug="dummy_post1",
                   is_published=False)
        dummy_post(title='Dummy post2', slug="dummy_post2",
                   is_published=False)
        dummy_post(title='Dummy post3', slug="dummy_post3",
                   is_published=False)
        response = self.tester.get('/drafts?page=2')
        self.assertIn(b'Dummy post1', response.data,
                      "Can't find the last dummy post on the second page of "
                      "the /drafts.")

    def test_pagination_for_search(self):
        """Will test pagination for our /search route.
        """
        dummy_post(title='Dummy post1', slug="dummy_post1",
                   is_published=True)
        dummy_post(title='Dummy post2', slug="dummy_post2",
                   is_published=True)
        dummy_post(title='Dummy post3', slug="dummy_post3",
                   is_published=True)
        response = self.tester.get('/search?page=2&q=dummy')
        self.assertIn(b'Dummy post3', response.data,
                      "Can't find the last dummy post on the second page of "
                      "the search results.")


class Posting(TestCase):
    """Contains tests pertaining to the creation and editing of posts.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        dummy_post(categories=['tiger', 'bird', 'dog'])

    def tearDown(self):
        self.app_context.pop()

    def test_posting_published(self):
        """Testing of the whole posting process starting from the /create page.

         This test concerns published posts.
        """
        with self.app.test_client() as tester:
            response = posting(tester, '/create_post',
                               categories_field_0='camel',
                               categories_field_1='elephant',
                               categories_field_2='rat')
            self.assertIn(b'Post is now live.', response.data,
                          "No message telling you your post went live.")
            self.assertEqual(request.path,
                             url_for('main.index'),
                             "Redirect to the post detail did not happen.")
            self.assertIn(b'test body', response.data,
                          "Test post can't be found on the /index page.")
            match = all(x in response.data for x in [b'camel', b'elephant',
                                                     b'rat'])
            self.assertTrue(match, "A category is missing from the"
                                   " published post.")

    def test_posting_drafts(self):
        """Testing of the whole posting process starting from /create_post .

         This test concerns drafts.
        """
        with self.app.test_client() as tester:
            response = posting(tester,
                               '/create_post',
                               title_field='test draft',
                               publish='')
            self.assertIn(b'Post saved as draft', response.data,
                          "No message telling you your draft was saved.")
            self.assertEqual(request.path, url_for('main.drafts'),
                             "Redirect to the /drafts page did not happen.")
        response = self.tester.get('/drafts')
        self.assertIn(b'test draft', response.data,
                      "Test draft can't be found on the /drafts page.")

    def test_access_drafts_non_logged(self):
        """Testing that a non-logged in user can't access drafts posts.
        """
        self.app.config['LOGIN_DISABLED'] = False
        post = Post.query.filter_by(slug='dummy_post').first_or_404()
        post.is_published = False
        response = self.tester.get('/dummy_post')
        self.assertEqual(response.status_code, 404,
                         "The draft post can still be accessed by a "
                         "non-logged in user.")

    def test_duplicate_titles(self):
        """Testing that a newly created post can't take the same title as an
         old post.
        """
        # The post that we will create use the same title as that
        # of the dummy post created in the setUp
        response = posting(self.tester,
                           '/create_post',
                           title_field='Dummy post',
                           content_field='test duplicate post title')
        self.assertIn(b'title is already in use', response.data,
                      "No message telling you that the title"
                      " is already in use.")
        response = self.tester.get('/')
        self.assertNotIn(b'test duplicate post title', response.data,
                         "Test post was still published and can be found"
                         " on the /index page")

    def test_edit_posts(self):
        """Testing of the whole editing process of a post starting from the
        /edit_post page.
        """
        # The post that we will edit is the one created in the setUp.
        # First we will test the process of publishing an edited post:
        with self.app.test_client() as tester:
            response = posting(tester,
                               '/dummy_post/edit_post',
                               title_field='test editing post')
            self.assertIn(b'edited and published', response.data,
                          "No message telling you your post"
                          " was successfully edited")
            self.assertEqual(request.path,
                             url_for('main.index'),
                             "Redirect to the homepage did not happen.")
        response = self.tester.get('/test_editing_post')
        self.assertIn(b'test editing post', response.data,
                      "Content of the edited post can't be found"
                      " on the detail page")
        # Finally we will test saving an edited post as a draft:
        with self.app.test_client() as tester:
            response = posting(tester,
                               '/test_editing_post/edit_post',
                               title_field='test editing draft',
                               publish='')
            self.assertIn(b'edited and saved', response.data,
                          "No message telling you your post"
                          " was successfully edited.")
            self.assertEqual(request.path, url_for('main.drafts'),
                             "Redirect to the /drafts page did not happen.")
        self.assertIn(b'test editing draft', response.data,
                      "Content of the edited post can't be found"
                      " on the /drafts page.")

    def test_prepopulate_edit_posts(self):
        """Testing that the input fields of the /<slug>/edit_post route are
        pre-populated.
        """
        response = self.tester.get('/dummy_post/edit_post')
        self.assertIn(b'Dummy post', response.data,
                      "The title field have not been pre-populated.")
        self.assertIn(b'Dummy Content', response.data,
                      "The content field have not been pre-populated.")
        match = all(x in response.data for x in [b'tiger', b'bird', b'dog'])
        self.assertTrue(match, "A category field have not been pre-populated.")
        self.assertIn(b'<input checked class="form-check-input" id="publish"',
                      response.data, "The ``Publish Now`` checkbox "
                                     "have not been checked.")

    def test_duplicate_title_for_edited_post(self):
        """Testing that an edited post can't take the same title as an existing
        post.
        """
        # First we will create a new post that we will edit later.
        dummy_post(title='Post to edit',
                   content="post content",
                   slug="post_to_edit")
        # We will then try to edit the newly created post so the title is the
        # same as the one we used for our dummy_post created in the setUp.
        response = posting(self.tester,
                           '/post_to_edit/edit_post',
                           title_field='Dummy post',
                           content_field='test duplicate post title')
        self.assertIn(b'title is already in use', response.data,
                      "No message telling you that the title"
                      " is already in use.")
        response = self.tester.get('/')
        self.assertNotIn(b'test duplicate post title', response.data,
                         "Test post with duplicate title was still published"
                         " and can be found on the /index page.")
        self.assertIn(b'post content', response.data,
                      "Content of the unedited test post can not be found"
                      " on the /index page.")


class PreviewPosts(TestCase):
    """Contains tests pertaining to the previewing of posts.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            dummy_post(categories=['tiger', 'bird', 'dog'])

    def test_preview_new_post(self):
        """Tests that we can preview a new post before publishing.

        This test concerns posts made with the /create route.
        """
        with self.app.test_client() as tester:
            response = posting(tester, '/create_post', preview='Preview')
            self.assertEqual(request.path,
                             url_for('main.preview', slug='test_title'),
                             "Redirect to the post preview did not happen.")
            self.assertIn(b'Preview of &#34;test title&#34;', response.data,
                          "Title does not tells us that we are on the"
                          " <slug>/preview page.")
            time = datetime.utcnow().strftime('%m/%d/%Y at %I:%M %p')
            time_ref = 'Posted ' + time
            self.assertIn(bytes(time_ref, 'utf-8'), response.data,
                          "Timestamp can not be found on the post preview.")

    def test_preview_edited_post(self):
        """Tests that we can preview an edited post before publishing.

        This test concerns posts made with the /<slug>/edit route.
        """
        with self.app.test_client() as tester:
            # Post to edit is the one created in SetUp.
            response = posting(tester,
                               '/dummy_post/edit_post',
                               title_field='test editing post',
                               preview='Preview')
            self.assertEqual(request.path,
                             url_for('main.preview', slug='test_editing_post'),
                             "Redirect to the post preview did not happen.")
            self.assertIn(b'Preview of &#34;test editing post&#34;',
                          response.data,
                          "Title does not tells us that we are on the"
                          " <slug>/preview page.")
            match = all(x in response.data for x in [b'tiger', b'bird', b'dog'])
            self.assertTrue(match,
                            "A category does not appear in the preview.")


class DeletePosts(TestCase):
    """Contains test to verify that we are capable to delete posts.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            dummy_post()

    def test_delete_post(self):
        """Testing to see if our /delete_post route can effectively delete a
        post.
        """
        with self.app.test_client() as tester:
            response = tester.post('/dummy_post/delete_post',
                                   follow_redirects=True)
            self.assertIn(b'Post deleted', response.data,
                          "No message telling you your dummy post "
                          "was deleted.")
            self.assertEqual(request.path, url_for('main.index'),
                             "Redirect to the /index page did not happen.")
        response = self.tester.get('/dummy_post')
        self.assertEqual(response.status_code, 404,
                         "Reaching the url for the deleted post"
                         " does not return a 404 error.")


class Search(TestCase):
    """Contains tests pertaining to the search functionality of our app.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            dummy_post()

    def test_search_post(self):
        """Testing a simple search query.
        """
        response = self.tester.get('/search?q=dummy')
        self.assertIn(b'Dummy Content', response.data,
                      "The post we're searching for is not showing up"
                      " in the search results.")

    def test_3_char_min(self):
        """Testing that we need 3 characters minimum to conduct a search.

        If not we are supposed to receive a message telling us to try
        again.
        """
        with self.app.test_client() as tester:
            response = tester.get('/search?q=me', follow_redirects=True)
            self.assertEqual(request.path, url_for('main.index'),
                             "Redirect to the /index page did not happen.")
            self.assertIn(b'Search string must have', response.data,
                          "No message asking you to try again.")

    def test_empty_search(self):
        """Testing that we are being informed when our search query returns
         nothing.
        """
        response = self.tester.get('/search?q=random')
        self.assertIn(b'did not return any results', response.data,
                      "No message telling you that your search query"
                      " did not return any result.")


class Sitemap(TestCase):
    """Contains tests for our sitemap.
    """
    def setUp(self):
        self.app = create_app(TestConfig)
        self.tester = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            dummy_post()
            dummy_post(title='Dummy Draft Post', slug="dummy_draft",
                       is_published=False)

    def test_post_presence(self):
        """Test that our published posts can effectively be found in the
        sitemap.
        """
        response = self.tester.get('/sitemap')
        self.assertIn(b'dummy_post', response.data,
                      "Test post can't be found in the sitemap.")


if __name__ == '__main__':
    unittest.main(verbosity=2)