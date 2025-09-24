"""Contains the Config class that wil be used to configure our app.
"""
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
"""
FlaskyPress Configuration Settings
----------------------------------

This file contains all configuration variables for the FlaskyPress application.

Core Settings:
    SECRET_KEY (str)
        A unique, secret value used to:
        - Protect web forms from CSRF attacks.
        - Cryptographically sign cookies for added security.

    SQLALCHEMY_DATABASE_URI (str)
        The database connection URL.
        Defaults to SQLite but can be configured to use PostgreSQL, MySQL,
        or any database supported by SQLAlchemy.

    SQLALCHEMY_TRACK_MODIFICATIONS (bool)
        Enables or disables SQLAlchemy's event notification system.
        This feature consumes extra resources and is generally unnecessary,
        so it should typically be set to False.

Site and Content Settings:
    SITE_NAME (str)
        The name of your site:
        - Displayed as branding in the navigation menu.
        - Used by the mail logger to identify the app in error reports.

    POSTS_PER_PAGE (int)
        The maximum number of posts displayed per page on the /index, /drafts,
        and /search pages.

    STYLE_EMBED (bool)
        When set to True, embeds are wrapped with Bootstrap 4 classes to make
        them responsive.

    COPYRIGHT (str)
        The copyright information displayed in the site footer.

    URL_PREFIX (str)
        Required only when running FlaskyPress from a subdirectory of your domain.
        Example:
            Root domain: www.mywebsite.com
            Subdirectory: www.mywebsite.com/subfolder/

Session Settings:
    SESSION_TYPE (str)
        Specifies the session interface type used by Flask-Session.
        Example: "filesystem", "redis", etc.

Search Configuration (Whooshee):
    WHOOSHEE_DIR (str)
        Directory where the search index is stored.
        Defaults to: app_root_folder/whooshee

    WHOOSHEE_MIN_STRING_LEN (int)
        Minimum number of characters required for a search query.
        Default: 3

    WHOOSHEE_WRITER_TIMEOUT (int)
        Time (in seconds) Whooshee will try to acquire a write lock.
        Default: 2

    WHOOSHEE_MEMORY_STORAGE (bool)
        Stores the search index in memory instead of writing it to a file.
        Typically set to True only during testing.
        Default: False

    WHOOSHEE_ENABLE_INDEXING (bool)
        Enables or disables search indexing operations.
        Default: True

Email Configuration (Error Reporting):
    These settings are only required if you want to receive email notifications
    when the application encounters errors. If MAIL_SERVER is not set, the mail
    logger will be disabled.

    MAIL_SERVER (str)
        The SMTP server address used to send error reports.
        Example: smtp.googlemail.com

    MAIL_PORT (int)
        The SMTP port used by your email service provider.
        Refer to your provider's documentation for the correct value.

    MAIL_USE_TLS (bool)
        Enables TLS encryption for outgoing emails to prevent eavesdropping.

    MAIL_USERNAME (str)
        The username for the email account that sends error reports.

    MAIL_PASSWORD (str)
        The password for the email account that sends error reports.

    ADMINS (list)
        A list of email addresses that should receive error notifications.
        Include your own address to ensure you receive alerts.

    FROM_ADDRESS (str)
        The email address displayed as the sender of error reports.
"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'sqlite:///' + os.path.join(basedir, 'blog.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SITE_NAME = os.environ.get('SITE_NAME') or 'FlaskyPress'
    POSTS_PER_PAGE = 10
    STYLE_EMBED = True
    COPYRIGHT = os.environ.get('COPYRIGHT') or 'FlaskyPress, &copy; 2019'
    URL_PREFIX = os.environ.get('URL_PREFIX') or ''
    SESSION_TYPE = 'filesystem'
    # config for whooshee search module
    WHOOSHEE_DIR = os.path.join(basedir, 'whooshee')
    WHOOSHEE_MIN_STRING_LEN = 3
    WHOOSHEE_WRITER_TIMEOUT = 2
    WHOOSHEE_MEMORY_STORAGE = False
    WHOOSHEE_ENABLE_INDEXING = True
    # config for the mail logging module.
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    FROM_ADDRESS = os.environ.get('FROM_ADDRESS')





