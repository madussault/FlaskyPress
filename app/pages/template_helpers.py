"""Integrates global functions for use in our templates.
"""
from app.pages import bp
from app.models import Post


@bp.app_template_global()
def page_exists():
    """Tells us if the db contains pages.

    return
    ------
        Post query object.
    """
    return Post.query.filter_by(is_page=True).first()


@bp.app_context_processor
def published_pages():
    """Get all published pages from the db.

    return
    ------
        Dictionary containing a list of the pages objects.
    """
    p = Post.query.filter_by(is_page=True, is_published=True).all()
    return dict(published_pages=p)



