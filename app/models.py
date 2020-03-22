"""Contains the models that will be used to define our database tables.
"""
from flask import Markup
from app import db, whooshee, login
from datetime import datetime
from slugify import slugify
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
# micawber_bs4_classes is a modified version of the micawber module:
# https://pypi.org/project/micawber/
# our version adds bootstrap 4 classes to the embeds and make them responsive.
from micawber_bs4_classes import bootstrap_basic, parse_html
from micawber_bs4_classes.cache import Cache as OEmbedCache
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Model for the table that will accept the admin password.

    Attributes
    ----------
    id : int
        This attribute is set automatically by SQLAlchemy
    password : str
        Set by the function ``set_password``
    """
    id = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        """Generates a hash from a given string.

        To store passwords in the database it is best to first conceal them
        using hashing.

        Parameters
        ----------
        password : str
            A string is taken from a user input at the moment of registration.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks a password against a given hashed password value.

        Parameters
        ----------
        password : str
            Is taken from a user input at the moment of login.

        Returns
        -------
        bool
            True if the password matched, False otherwise.
        """
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    """Reloads a user from a session by querying it's id from the database.

    Flask-Login keeps track of the logged in user by storing its unique
    identifier in Flask's user session. The module is not capable by itself
    to load a user from a model database. For that we use the
    @login.user_loader decorator, which will load a user given the
    ID. The function decorated with user_loader decorator will be called
    every time a request comes to the server. It loads the user from the user
    ID stored in the session cookie. Flask-Login makes the loaded user
    accessible via the ``current_user`` proxy.

    Parameters
    ----------
    id : str
        Id of the logged in user.

    Returns
    -------
    class 'app.models.User'
        A user object, or None if the user does not exist.
    """
    return User.query.get(int(id))


class PostCategory(db.Model):
    """Association table linking the Post and Category models.

    They share a many-to-many relationship.

    parameters
    ----------
    id : int
        This attribute is set automatically by SQLAlchemy
    post_id : int
        Id of the post in the association
    category_id : int
        Id of the category in the association
    """
    __tablename__ = 'post_category'
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


# Configure micawber_bs4_classes with the default OEmbed providers
# (YouTube, Flickr, etc). We'll use a simple in-memory cache so that
# multiple requests for the same video don't require multiple network requests.
oembed_providers = bootstrap_basic(OEmbedCache())


def util_html_content(self):
    """Converts markdown into html and media urls into embeds.

    Generates HTML representation of the markdown-formatted blog entry, and
    also convert any media URLs into rich media objects such as video
    players or images.

    Returns
    -------
    class 'flask.Markup'
      Returns markup objects so that the passed string can't be double
      escaped.
    """
    hilite = CodeHiliteExtension(linenums=False)
    extras = ExtraExtension()
    markdown_content = markdown(self.content,
                                extensions=[hilite, extras])
    oembed_content = parse_html(
        markdown_content,
        oembed_providers,
        urlize_all=True)
    # If your returned 'oembed_content' without using 'Markup()' the html
    # would be shown as text on the page instead of being rendered.
    return Markup(oembed_content)


# When we pass the name of a model variable to this decorator, the content
# in the database associated with that variable become indexed and at the same
# time searchable.
@whooshee.register_model('title', 'content')
class Post(db.Model):
    """Model for the table that will accept the content of blog posts.

    This model is also used for pages.

    Attributes
    ----------
     id : int
        Each post is assigned a unique numerical id starting from 1.
    title : str
        Post title.
    content : str
        Post body.
    slug : str
        URL-friendly representation of the entry's title.
    published : bool
        Indicate whether the post is published or a draft.
    timestamp : class 'datetime.datetime'
        Time and date of the post creation.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String(40000))
    slug = db.Column(db.String(150), unique=True, index=True)
    is_page = db.Column(db.Boolean)
    is_published = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    categories = db.relationship('Category', secondary='post_category',
                                 backref='post', lazy='dynamic',
                                 order_by='Category.name')

    @property
    def html_content(self):
        """See documentation of ``util_html_content``.
        """
        return util_html_content(self)

    def slugify_title(self):
        """Generates a URL-friendly representation of the entry's title.
        """
        self.slug = slugify(self.title, lowercase=True, separator="_")

    def __repr__(self):
        return f'<Post: {self.title}>'


class Category(db.Model):
    """Model for the table that will accept the accepts post's categories.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    slug = db.Column(db.String(45))
    posts = db.relationship('Post', secondary='post_category',
                            backref='category', lazy='dynamic')

    def slugify_name(self):
        """Generates a URL-friendly representation of the category's name.
        """
        self.slug = slugify(self.name, lowercase=True, separator="_")

    def __repr__(self):
        return f'<Category: {self.name}>'


def reorder_widgets():
    """Takes an existing widget order and modify it to remove gaps.

    Example, the following widget order:

    "content widget 1" :: 1
    "Search Bar Widget" :: 3
    "Category Widget" :: 4

    Becomes:

    "content widget 1" :: 1
    "Search Bar Widget" :: 2
    "Category Widget" :: 3
    """
    wo = (WidgetOrder.query.order_by(WidgetOrder.position))
    if wo:
        for index, obj in enumerate(wo):
            obj.position = index + 1
        db.session.commit()


def add_to_or_remove_from_sidebar_util(status, value, widget_name):
    """Add to or remove a widget from the sidebar.

    - When a widget is first added to the sidebar the function sets it's
    default position. The default position is always at the end of the other
    widgets.

    - The function also removes a widget from the sidebar if a user decides to
    change it's placement. When this action occurs a reordering of the widgets
    is also triggered to remove gaps between positions.

    parameters
    ----------
    status : str
        Represent the choice made by the user as to where the widget should be
        placed.
    value : str
        If a user choose to have his widget in the sidebar the value entered
        in the table should match this one.
    widget_name : str
        Name of the widget.
    """
    wo = WidgetOrder.query.filter_by(name=widget_name)
    if status == value:
        if not wo.first():
            widgets_count = WidgetOrder.query.count()
            new_wo = WidgetOrder(name=widget_name,
                                 position=widgets_count + 1)
            db.session.add(new_wo)
            db.session.commit()
    else:
        if wo.first():
            wo.delete()
            db.session.commit()
            reorder_widgets()


class SearchBarControls(db.Model):
    """This model concerns the placement of the search bar.
    """
    id = db.Column(db.Integer, primary_key=True)
    placement = db.Column(db.String(50))

    def add_to_or_remove_from_sidebar(self):
        """See documentation of ``add_to_or_remove_from_sidebar_util``.
        """
        add_to_or_remove_from_sidebar_util(self.placement, 'sidebar',
                                           'Search Bar Widget')

    def __repr__(self):
        return f'<Search bar placement: {self.placement}>'


class CategoriesControls(db.Model):
    """This model concerns the arrangement of the categories in the layout.
    """
    id = db.Column(db.Integer, primary_key=True)
    presence = db.Column(db.String(50))

    def add_to_or_remove_from_sidebar(self):
        """See documentation of ``add_to_or_remove_from_sidebar_util``.
        """
        add_to_or_remove_from_sidebar_util(self.presence, 'sidebar_and_posts',
                                           'Category Widget')

    def __repr__(self):
        return f'<Where are displayed categories: {self.presence}>'


class ContentWidget(db.Model):
    """Model for the table that will accept input defining our content widgets.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75))
    slug = db.Column(db.String(75), unique=True, index=True)
    content = db.Column(db.String(5000))
    is_published = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @property
    def html_content(self):
        """See documentation of ``util_html_content``.
        """
        return util_html_content(self)

    def slugify_title(self):
        """Generates a URL-friendly representation of the widget's title.
        """
        self.slug = slugify(self.title, lowercase=True, separator="_")

    def add_to_or_remove_from_sidebar(self):
        """See documentation of ``add_to_or_remove_from_sidebar_util``.
        """
        add_to_or_remove_from_sidebar_util(self.is_published, True, self.title)

    def remove_from_sidebar(self):
        """Clear content widget from the sidebar.
        """
        WidgetOrder.query.filter_by(name=self.title).delete()
        db.session.commit()
        reorder_widgets()

    def remove_invalid_title_from_sidebar(self, original_title):
        """Remove from the sidebar the reference to the old title of an edited
        widget.

        parameter
        ---------
        original_title : str
            Title of the content widget before editing.
        """
        if self.title != original_title:
            WidgetOrder.query.filter_by(name=self.title).delete()
            db.session.commit()

    def __repr__(self):
        return f'<Content widget title: {self.title}>'


class Social(db.Model):
    """Model for the table that will accept the user social addresses.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(500))

    def __repr__(self):
        return f'<Social address: {self.name}: {self.address}>'


class WidgetOrder(db.Model):
    """This model concerns the order of the widgets in the sidebar.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    position = db.Column(db.String(2))

    def __repr__(self):
        return f'<Widget name and position: {self.name}: {self.position}>'

