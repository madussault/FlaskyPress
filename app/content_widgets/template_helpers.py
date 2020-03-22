"""Integrates global functions and filters for use in our templates.
"""
from app.content_widgets import bp
from app.models import ContentWidget


@bp.app_template_global()
def content_widget_exists():
    """Used to verify if any sidebar content widget exists in our db.
    """
    return ContentWidget.query.first()


@bp.app_template_filter()
def get_content_widget(widget_title):
    """Get specific sidebar content widget object from the db.

    parameter
    ---------
    widget_title : str
        Represents the title of the content widget we are looking for.
    """
    return ContentWidget.query.filter_by(title=widget_title).first()





