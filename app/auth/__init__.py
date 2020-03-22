"""Registers the ``auth`` package as a flask blueprint.

This blueprint will handle the authentication process of the app:
registration, login and logout.
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes


