"""Register the ``main`` package as a flask blueprint

This blueprint integrate most the the features and the pages comprising our
app:

- Creating new posts and drafts.
- Previewing a newly created or edited post.
- Viewing the detail of an existing post or a draft.
- Editing existing posts and drafts.
- Deleting a post or a draft.
- Listing published posts and drafts.
- Searching posts.
- Sitemap.
"""

from flask import Blueprint
from app import db

bp = Blueprint('main', __name__)


@bp.before_app_first_request
def create_db():
    """Create the production database if it is not existing already.
    """
    db.create_all()


from app.main import routes, template_helpers
