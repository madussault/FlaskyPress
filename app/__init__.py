"""
    FlaskyPress
    -----------

    FlaskyPress is a basic blogging app created as a starter project to learn
    programming. New features will be added overtime.

    :copyright: 2019 madussault
    :license: MIT License,
              https://github.com/madussault/FlaskyPress/blob/master/LICENCE.txt
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from flask_login import LoginManager
from flask_session import Session
from app.debugging import mail_logger, logging_to_file


db = SQLAlchemy()
whooshee = Whooshee()
login = LoginManager()
sess = Session()


def create_app(config_class=Config):
    """Create a flask application instance.

    Parameters
    ----------
    config_class
        Here is loaded the Config class containing all the
        configuration parameters needed by flask and it's extensions to run
        our application. When tests are going to be run a different class
        containing custom parameters for the tests are going to be passed to
        this function instead of the production one.

    Returns
    -------
    Your app object.
        When our app goes live, this object will be created in the ``launch.py``
        file, the script used to start our app.
    """
    # If we are using nginx to serve static files and our application
    # is placed in a domain subdirectory, we need to specify the url path
    # for the static folder or else our css, images, js, etc will become
    # inaccessible to the app.
    blog = Flask(__name__, static_url_path=f'{config_class.URL_PREFIX}/static')
    blog.config.from_object(config_class)

    db.init_app(blog)
    whooshee.init_app(blog)
    login.init_app(blog)
    sess.init_app(blog)

    # Non logged in users trying to reach page protected by @login_required
    # will be redirected to the 'login' page.
    login.login_view = 'auth.login'
    # Set the color for the flash messages served by flask-login.
    login.login_message_category = "warning"

    from app.main import bp as main_bp
    blog.register_blueprint(main_bp, url_prefix=config_class.URL_PREFIX)

    from app.errors import bp as errors_bp
    blog.register_blueprint(errors_bp, url_prefix=config_class.URL_PREFIX)

    from app.auth import bp as auth_bp
    blog.register_blueprint(auth_bp, url_prefix=config_class.URL_PREFIX)

    from app.controls import bp as controls_bp
    blog.register_blueprint(controls_bp, url_prefix=config_class.URL_PREFIX)

    from app.pages import bp as pages_bp
    blog.register_blueprint(pages_bp, url_prefix=config_class.URL_PREFIX)

    from app.categories import bp as categories_bp
    blog.register_blueprint(categories_bp, url_prefix=config_class.URL_PREFIX)

    from app.content_widgets import bp as content_widgets_bp
    blog.register_blueprint(content_widgets_bp,
                            url_prefix=config_class.URL_PREFIX)

    mail_logger(blog)
    logging_to_file(blog)

    return blog


# This import is at the bottom to avoid circular dependencies.
from app import models





