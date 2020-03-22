"""Registers the ``content_widgets`` package as a flask blueprint.

This blueprint integrates the use of content widgets in our blog sidebar. These
widgets can be used to display most of what can usually be displayed inside a
blog post.
"""

from flask import Blueprint

bp = Blueprint('content_widgets', __name__)

from app.content_widgets import routes, template_helpers
