from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, StringField
from wtforms.validators import DataRequired, Length


class PageForm(FlaskForm):
    """This form will be used to create and edit pages.

    Attributes
    ----------
    title_field : class wtforms.fields.StringField
        Title for the page goes here.
    body_field : class wtforms.fields.TextAreaField
        Content body for the page goes here.
    publish : class wtforms.fields.BooleanField
        If this box is checked the page will be published. If not it will be
        made inaccessible to the non-logged in users.
    save : class wtforms.fields.SubmitField
        Submit the form to the route.
    """
    title_field = StringField('Page title...',
                              render_kw={'class': 'form-control'},
                              validators=[DataRequired(),
                                          Length(min=1, max=30)]
                              )
    content_field = TextAreaField('Page body...',
                                  render_kw={'rows': 10,
                                             'class': 'form-control'},
                                  validators=[DataRequired(),
                                              Length(min=1, max=40000)]
                                  )
    publish = BooleanField('Publish Now',
                           render_kw={'class': 'form-check-input'}
                           )
    # The 'create' label will be for new pages and the 'save' label will
    # be for editing them.
    create = SubmitField('Create',
                         render_kw={'class': 'btn btn-primary mr-1'}
                         )
    save = SubmitField('Save',
                       render_kw={'class': 'btn btn-primary mr-1'}
                       )
    preview = SubmitField('Preview',
                          render_kw={'class': 'btn btn-secondary mr-1',
                                     'formtarget': '_blank'}
                          )
