"""Registers the ``categories`` package as a flask blueprint.

This blueprint integrates the use of categories in our blog.
"""
from flask import Blueprint

bp = Blueprint('categories', __name__)

from app.categories import routes, template_helpers


