"""Handle error 404 and 500.

Allow to serve custom pages when such errors occurs.
"""

from flask import render_template
from app.errors import bp
from app import db


@bp.app_errorhandler(404)
def not_found_error(error):
    """Serves custom template to the user when a code 404 error occurs.

    Parameters
    ----------
    error : int
        The error code as an integer for the handler.
    """
    title = "Error 404"
    return render_template('errors/404.html', title=title), 404


@bp.app_errorhandler(500)
def internal_error(error):
    """Serves custom template to the user when a code 500 error occurs.

    Parameters
    ----------
    error : int
        The error code as an integer for the handler.
    """
    db.session.rollback()
    return render_template('errors/500.html'), 500
