"""Contains set of functions often reused throughout the app.
"""
from app.models import Category
from app import db


def set_categories(fields):
    """Set the names of the category a blog entry will be posted under.

    The function receives user inputs from the ``categories_field`` at the
    moment of the post creation and if no proper category name is given the
    function will not return anything (and later on the post will be put under
    the ``uncategorized`` category.).

    parameter
    ----------
    fields: list
        Contains user inputs representing category names.

    return
    ------
    post_categories: list
        Contains the names of the categories a blog entry will be poster under.
    """
    post_categories = []
    for name in set(fields):
        existing_category = Category.query.filter_by(name=name).first()
        if name in ['', 'uncategorized']:
            pass
        elif existing_category:
            post_categories.append(existing_category)
        else:
            c = Category(name=name.strip())
            c.slugify_name()
            post_categories.append(c)
    return post_categories


def del_unused_categories():
    """Will delete from the db all the category names not attached to a post.
    """
    Category.query.filter_by(posts=None).delete(synchronize_session=False)
    db.session.commit()


def disassociate_categories(post_object):
    """Will remove the relationship between a post and all of it's categories.

    If we simply delete the post without running this function the relationship
    is going to stay in the association table of the ``PostCategory`` model.

    parameter
    ----------
    post_object: SQLAlchemy query object
        Contains post data queried from the db.
    """
    post = post_object.first()
    post.categories = []


