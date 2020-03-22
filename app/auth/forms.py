"""Contains forms used in the authentication process.

Contains a registration and a login form. Flask-WTF was used to define
the forms.
"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegistrationForm(FlaskForm):
    """The form used to register the blog admin.

    This form is rendered on the /register page. The only data it accepts is a
    new password. This password will be used by the admin to log inside
    the app.

    Attributes
    ----------
    pass_field1 : class wtforms.fields.PasswordField
        Form field accepting a string user input that will be used as a
        password.
    pass_field2 : class wtforms.fields.PasswordField
        The string entered here is to confirm the choice of password made by
        the user. For the form to validate the user input passed here and at
        pass_field1 must be equal.
    submit : class wtforms.fields.SubmitField
        Submit the form to the route.

    """
    pass_field1 = PasswordField('Enter password...',
                                render_kw={'class': 'form-control'},
                                validators=[DataRequired()]
                                )
    pass_field2 = PasswordField('Repeat password...',
                                render_kw={'class': 'form-control'},
                                validators=[DataRequired(),
                                            EqualTo('pass_field1',
                                                    message='Both password strings must match.')]
                                )
    submit = SubmitField('Register',
                         render_kw={'class': 'btn btn-primary btn-block'}
                         )


class LoginForm(FlaskForm):
    """The form used on the /login page to log into the app.

    Attributes
    ----------
    pass_field : class wtforms.fields.PasswordField
        Form field accepting a string user input. A password is expected to
        be entered here for logging in.
    remember_me : class wtforms.fields.BooleanField
        Checkbox used to command the app to remember the user session.
    submit : class wtforms.fields.SubmitField
        Submit the form to the route.
    """
    pass_field = PasswordField('Password',
                               render_kw={'class': 'form-control mb-2',
                                          'id': 'pass_field',
                                          'placeholder': 'Password...'},
                               validators=[DataRequired()]
                               )
    remember_me = BooleanField('Remember Me',
                               render_kw={'class': 'form-check-input'}
                               )
    submit = SubmitField('Log in',
                         render_kw={'class': 'btn btn-primary mb-2'}
                         )
