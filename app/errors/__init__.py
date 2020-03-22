"""Register the ``errors`` package as a flask blueprint

This blueprint will handle 404 and 500 errors and will determine what will be
shown to the user when such error occurs.
"""

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
