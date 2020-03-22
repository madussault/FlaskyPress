"""Set the logger to email you error reports and to write info to log.
"""

import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os


def mail_logger(app):
    """ Set the ``logging`` module to send you error reports by emails.

    Logging messages which are at the ERROR level or more severe will be send
    to you by email on the form of a traceback.
    """
    # For this function to work the attributes of the config section
    # 'config for the mail logging module' must be all set.
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config["FROM_ADDRESS"],
                toaddrs=app.config['ADMINS'], subject=f'{app.config["SITE_NAME"]} Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)


def logging_to_file(app):
    """Set the logger to write debugging infos to log.
    """
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = RotatingFileHandler(f'logs/{app.config["SITE_NAME"]}.log',
                                           maxBytes=10240, backupCount=10)
        # Set custom formatting for the log messages
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{app.config["SITE_NAME"]} startup')

