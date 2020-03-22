"""Registers the ``controls`` package as a flask blueprint.

This blueprint integrates options to further configure what is being
 displayed on our blog and how they are being displayed. Among them:

- Where are the categories shown in our pages.
- Where to place the search bar in the layout.
- In what order should the widgets be displayed in the sidebar.
- Which social addresses to display in the footer.
"""

from flask import Blueprint
from app import db
from app.models import SearchBarControls, CategoriesControls, Social
from app.controls.dicts import socials

bp = Blueprint('controls', __name__)


@bp.before_app_first_request
def default_search_bar_placement():
    """Set the default placement of the search bar in the layout.

    Will take effect when the blog is accessed for the first time.
    """
    if not SearchBarControls.query.first():
        s = SearchBarControls(placement="navbar")
        db.session.add(s)
        db.session.commit()


@bp.before_app_first_request
def default_categories_presence():
    """Set where the categories are going to be displayed in our pages by
    default.

    Will take effect when the blog is accessed for the first time.
    """
    if not CategoriesControls.query.first():
        c = CategoriesControls()
        c.presence = "sidebar_and_posts"
        c.add_to_or_remove_from_sidebar()
        db.session.add(c)
        db.session.commit()


@bp.before_app_first_request
def default_socials():
    """Registers all selected social media names and assigns them blank
    addresses.

    Will take effect when the blog is accessed for the first time.
    """
    if not Social.query.first():
        for item in socials.items():
            s = Social()
            s.name = item[1][0]
            s.address = ''
            db.session.add(s)
        db.session.commit()


from app.controls import routes, template_helpers
