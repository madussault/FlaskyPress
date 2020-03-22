"""Forms for creating new posts and pages.
"""
from flask_wtf import FlaskForm
from wtforms import (SubmitField, TextAreaField, BooleanField, StringField,
                     FieldList)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """This form will be used to create new posts and pages and also to
    edit them.

    Attributes
    ----------
    title_field : class wtforms.fields.StringField
        Post title goes here.
    content_field : class wtforms.fields.TextAreaField
        Post body goes here.
    publish : class wtforms.fields.BooleanField
        If this box is checked the post will be published. If not it will be
        saved as a draft.
    create : class wtforms.fields.SubmitField
        Submit the form to the route. This field will be used on the /create
        page only.
    save : class wtforms.fields.SubmitField
        Submit the form to the route. This field will be used on the
         /<slug>/edit_post page only.
    """
    title_field = StringField('Post title...',
                              render_kw={'class': 'form-control'},
                              validators=[DataRequired(),
                                          Length(min=1, max=150)]
                              )
    content_field = TextAreaField('Post content...',
                                  render_kw={'rows': 10,
                                             'class': 'form-control'},
                                  validators=[DataRequired(),
                                              Length(min=1, max=40000)]
                                  )
    categories_field = FieldList(StringField(
        'Categories: ',
        render_kw={'class': 'form-control',
                   'id': 'category_field',
                   'aria-describedby': 'passwordHelpBlock',
                   'aria-label': 'Categories'}
    ),
        min_entries=3
    )
    publish = BooleanField('Publish Now',
                           render_kw={'class': 'form-check-input'}
                           )
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

