"""Contains the Config class that wil be used to configure our app.
"""
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
# Will load the environment variables from the .env file that will
# then be assigned to the attributes in our Config class. If we store
# these config parameters in a .env file it is to prevent them from
# being uploaded to github by accident.
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """ Contains the config parameters that will be used by our app.

        These parameters will be used by flask and it's extensions. Some of
        them will also be used with modules unrelated to flask, for example
        the logging module used to send crash reports by email.

        Attributes
        ----------
        SECRET_KEY : str
            Input your own unique and secret key here. Will protect web forms
            against CSRF attack and is also used to signs the cookies
            cryptographically.
        SQLALCHEMY_DATABASE_URI : str
            Path to the database.
        SQLALCHEMY_TRACK_MODIFICATIONS : bol
            Flask-SQLAlchemy has its own event notification system that gets
            layered on top of SQLAlchemy. It takes extra resource and we
            don't need it.
        SITE_NAME : str
            Will show up as site branding in the menu.

            Will also be used by the mail logger to identify our app when an
            error message is being sent.
        POSTS_PER_PAGE : int
            Maximum post per page to show on the /index, /drafts and /search
            pages.
        STYLE_EMBED : bol
            If set to True will wrap embeds with bootstrap 4 classes and make
            them responsive.
        COPYRIGHT : str
            Copyright info that will be shown in the footer.
        URL_PREFIX : str
            Only needed when we want to run our app from a domain subdirectory,
            ex: www.my_website.com/subfolder/ instead of www.my_website.com .
        SESSION_TYPE : str
            Command the type of session interface the Flask-session extension
            is going to use.
        WHOOSHEE_DIR : str
            Folder to store the search index. (Default to
            app_root_folder/whooshee.)
        WHOOSHEE_MIN_STRING_LEN : int
            Min. characters for the search string (defaults to 3)
        WHOOSHEE_WRITER_TIMEOUT : int
            How long should whoosh try to acquire write lock? (defaults to 2)
        WHOOSHEE_MEMORY_STORAGE : bol
            Use the memory as storage instead of writing the search index to
            file. Will be set to True for tests. (defaults to False)
        WHOOSHEE_ENABLE_INDEXING : bol
            Specify whether or not to actually do any operations with the
            Whoosh index (defaults to True).
        MAIL_SERVER : str
            Address of the email server our mail logger is going to use to send
            our reports in case of error (ex, smtp.googlemail.com). If
            this value is not set the mail logger will be disabled.
        MAIL_PORT : int
            Port used by the mail server of your email service provider.
            Consult their website to find out.
        MAIL_USE_TLS : bol
            Enable encryption when sending email, which prevent eavesdropping.
        MAIL_USERNAME : str
            Username for the email account sending the error reports.
        MAIL_PASSWORD : str
            Password for the email account sending the error reports.
        ADMINS : list
            Here we store a list of the email addresses that will receive error
             reports, so your own email address should be in that list.
        FROM_ADDRESS : str
            Email address of the sender.
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





