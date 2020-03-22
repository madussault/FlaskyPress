from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, StringField
from wtforms.validators import DataRequired, Length


class ContentWidgetForm(FlaskForm):
    """Form for creating and editing content widgets.

    attributes
    ----------
    title_field : WTforms StringField object
        Form field accepting a string user input that will be used as a
        content widget title.
    content_field : WTforms TextAreaField object
        Form field accepting a string user input that will be used as the body
        of a content widget.
    publish : WTforms BooleanField object
        If this box is checked the content widget will be published. If not it
        will be saved as a draft.
    create : WTforms SubmitField object
        Submit the form to the route.
    save : WTforms SubmitField object
        Submit the form to the route.
    """
    title_field = StringField('Widget title...',
                              render_kw={'class': 'form-control'},
                              validators=[DataRequired(),
                                          Length(min=1, max=75)]
                              )
    content_field = TextAreaField('Widget body...',
                                  render_kw={'rows': 10,
                                             'class': 'form-control'},
                                  validators=[DataRequired(),
                                              Length(min=1, max=5000)]
                                  )
    publish = BooleanField('Publish now.',
                           render_kw={'class': 'form-check-input'}
                           )
    # The 'create' label will be for new content widgets and the 'save' label
    # will be for editing them.
    create = SubmitField('Create',
                         render_kw={'class': 'btn btn-primary mr-1'}
                         )
    save = SubmitField('Save',
                       render_kw={'class': 'btn btn-primary mr-1'}
                       )

