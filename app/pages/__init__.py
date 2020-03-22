"""Registers the ``pages`` package as a flask blueprint.

This blueprint integrates the use of pages in our application. These pages
will be displayed in the top navigation bar.
"""

from flask import Blueprint

bp = Blueprint('pages', __name__)

from app.pages import routes, template_helpers
