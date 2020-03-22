"""Contains helper functions for our tests.
"""

from app import db
from app.models import (Post, User, ContentWidget, CategoriesControls, Social,
                        SearchBarControls, WidgetOrder, Category)
from app.categories.utils import set_categories


def dummy_post(title='Dummy post', content="Dummy Content", slug="dummy_post",
               is_page=False, categories=[], is_published=True):
    """Will directly write to the database a dummy post for our tests.

    Parameters
    ----------
    title : str
        Post title.
    content : str
        Post content.
    slug : str
        Url friendly representation of the post title.
    is_page : bool
        We are using this function to publish both posts and pages. This
        parameter draws the difference between the two.
    categories : list
        List of categories the post will be published under.
    is_published : bool
        Whether the post will be published or saved as a draft.

    Return
    -------
    Post model object
        Contains post data.
    """
    c = set_categories(categories)
    post = Post(title=title,
                content=content,
                slug=slug,
                is_page=is_page,
                categories=c,
                is_published=is_published)
    db.session.add(post)
    db.session.commit()
    return post


def dummy_user():
    """Will directly write to the database a dummy user for our tests.

    Return
    -------
    User model object
        Contains user data.
    """
    user = User()
    user.set_password('pass')
    db.session.add(user)
    db.session.commit()
    return user


def dummy_content_widget(title='Dummy Content Widget', content="Dummy Content",
                         slug="dummy_content_widget", is_published=True):
    """Will directly write to the database a dummy content widget for our
     tests.

    Parameters
    ----------
    title : str
        Widget title.
    content : str
        Widget content.
    slug : str
        Url friendly representation of the widget title.
    is_published : bool
        Whether the widget will be published or not.

    Return
    -------
    ContentWidget model object.
        Contains data of the content widgets.

    """
    cw = ContentWidget(title=title,
                       content=content,
                       slug=slug,
                       is_published=is_published)
    db.session.add(cw)
    db.session.commit()
    return cw


def login(client, password="pass", ):
    """Helper function to log into our app.

    Parameters
    ----------
    client : test client object
        Passed here is the flask test client used to send the request.

    password : str
        Dummy password for logging into the app.

    Return
    -------
    post request object
        The test client is instructed to send a post request to the /login
        route. The request contains the fields values to be posted by the form.
    """
    return client.post('/login',
                       data=dict(pass_field=password, remember_me=True),
                       follow_redirects=True)


def posting(client, route, title_field='test title', content_field='test body',
            is_page=False, categories_field_0='', categories_field_1='',
            categories_field_2='', publish='yes', preview=None):
    """Helper function to create/edit posts and drafts by posting to our
    routes.

    This helper function also works for pages.

    Parameters
    ----------
    client : test client object
        Passed here is the flask test client used to send the request.
    route : str
        The route to where our request is going to be sent.
    title_field : str
        Post title passed to our form.
    content_field : str
        Post content passed to our form.
    is_page: bool
        Is the posting for a post or a page?
    categories_field_x : str
        Name of the categories passed to our form. A maximum of 3 are accepted.
        Their corresponding parameters are suffixed with a number from 0 to 2.
    publish : str
        Whether the post will be published or saved as a draft. This
        parameter represent the checkbox in our form. Using a string means
        the checkbox is ticked. Using an empty string means it is not checked.
    preview : str
        If a string is passed using this parameter our route is going to
        redirect us to the /preview route.

    Return
    -------
    post request object
        The test client is instructed to send a post request to a given
        route. The request contains the fields values to be posted by the form.
    """
    return client.post(route, data={
        'title_field': title_field,
        'content_field': content_field,
        'publish': publish,
        'is_page': is_page,
        'categories_field-0': categories_field_0,
        'categories_field-1': categories_field_1,
        'categories_field-2': categories_field_2,
        'preview': preview
    },
                            follow_redirects=True)


def add_category(name):
    """Write a category directly to the db.

    Parameters
    ----------
    name : str
        The name given to the category.

    Return
    -------
    c : Category model object
        Contains the data pertaining to the category.
    """
    c = Category(name=name)
    c.slugify_name()
    db.session.add(c)
    db.session.commit()
    return c


def add_social(name, address):
    """Write a social address directly to the db.

    Parameters
    ----------
    name : str
        Name of the service.

    address : str
        Address of the account.
    """
    s = Social(name=name, address=address)
    db.session.add(s)
    db.session.commit()


def control_search_bar(choice):
    """Write the search bar placement directly to the db.

    Parameters
    ----------
    choice : str
        Determine the placement's choice.
    """
    sbc = SearchBarControls(placement=choice)
    db.session.add(sbc)
    db.session.commit()


def control_categories(choice):
    """Write directly to the db where to display categories in the layout.

    Parameters
    ----------
    choice : str
        Determine where the user want the categories to be displayed.
    """
    cc = CategoriesControls(presence=choice)
    db.session.add(cc)
    db.session.commit()


def set_widgets_positions_in_sidebar(kwargs):
    """Assign to each widget name a position in the sidebar.

    Parameters
    ----------
    kwargs : Dictionary
        Contains the name of the widgets and their positions.
    """
    for name, position in kwargs.items():
        wo = WidgetOrder(name=name, position=position)
        db.session.add(wo)
    db.session.commit()


def dict_of_widgets_positions_in_sidebar():
    """Query the table of the ``WidgetOrder`` model and returns the result as a
     dict.

    return
    ------
    dict_of_query : dict
        The dictionary contains the name of the sidebar's widgets and
        their position.
    """
    query = (WidgetOrder.query.order_by(WidgetOrder.position).all())
    dict_of_query = {}
    for obj in query:
        dict_of_query[obj.name] = obj.position
    return dict_of_query


def add_three_dummy_widget_positions():
    """Will add 3 dummy widgets in the sidebar in a specific order.
    """
    wo1 = WidgetOrder(name='Search Bar Widget', position='1')
    wo2 = WidgetOrder(name='Dummy Content Widget', position='3')
    wo3 = WidgetOrder(name='Category Widget', position='2')
    db.session.add_all([wo1, wo2, wo3])
    db.session.commit()




