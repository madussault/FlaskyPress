from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import WidgetOrder
from slugify import slugify
from app.controls.dicts import socials


class SearchBarControlsForm(FlaskForm):
    """Form letting us choose where to place the search bar in the layout.

    attributes
    ----------
    placement_field : WTforms RadioField object
        Form field that will be rendered as a choice menu by the browser. Each
        choice is a tuple containing:
        - The name of the choice that will be entered in the db.
        - And a brief description of the choice offered to the user.
    """
    placement_field = RadioField('Where do you want the search bar'
                                 ' to be placed ?',
                                 choices=[("navbar", "In the navigation bar."),
                                          ("sidebar", "In the sidebar."),
                                          ("no_search", "Remove search bar.")],
                                 validators=[DataRequired()]
                                 )


class CategoriesControlsForm(FlaskForm):
    """Form letting us choose where to display the categories in our pages.

    attributes
    ----------
    presence_field : WTforms RadioField object
        Form field that will be rendered as a choice menu by the browser. Each
        choice is a tuple containing:
        - The name of the choice that will be entered in the db.
        - And a brief description of the choice offered to the user.
    """
    presence_field = RadioField('Where should the categories be displayed?',
                                choices=[("sidebar_and_posts",
                                          "In a sidebar widget and in the "
                                          "posts."),
                                         ("posts_only", "In the posts only."),
                                         ("no_categories",
                                          "Categories should not be displayed"
                                          " anywhere.")],
                                validators=[DataRequired()]
                                )


class SocialsForm(FlaskForm):
    """Allow the user to input the addresses of the social medias he has a
    presence.

    notes
    -----
        The fields for this form are dynamically created by the
        ``dynamic_social_fields`` function when the app first start.
    """


def dynamic_social_fields():
    """Create the fields used by ``SocialsForm``.
    """
    for key, value in socials.items():
        setattr(SocialsForm, f'{key}_address',
                StringField(value[0],
                            render_kw={'class': 'form-control ml-auto',
                                       "placeholder": value[1]}))


dynamic_social_fields()


class BaseWidgetsOrderForm(FlaskForm):
    """
    """


def position_choices():
    """Returns the choices that will be served by the form ordering our
    widgets.

    The function will dynamically create the choices for the WTForms field
    ``SelectField`` used in the form created by ``widgets_order_form``.

    return
    ------
    choices: list
        This list is made of tuples each containing a (value/label) pair.
    """
    choices = []
    for wo in WidgetOrder.query.all():
        choices.append((wo.position, wo.position))
    return choices


def prevent_identical(form, field):
    """Custom validator for the form ordering our widgets.

    A choice can be assigned to no more than 1 widget.
    """
    for f in form:
        if f.data == field.data and f.name != field.name:
            raise ValidationError('Choices must be distinct.')


def widgets_order_form():
    """Will dynamically create the form we use to re-order our widgets in the
    sidebar.

    The form can't be hardcoded because the positions change according to
    several conditions. Ex:
    - A newly published widget will be given a new default position which will
    increase the number of choices.
    - A non published/deleted widget will be removed from the sidebar which
    will decrease the number of choices and also possibly leave a gap in the
    order. Were this to happen the remaining widgets will be re-ordered
    (1-2-4 need to be changed to 1-2-3).

    return
    ------
    form : form object
        Form will let us choose, with the help of a menu, a position for each
        widget in the sidebar.
    """
    class Form(BaseWidgetsOrderForm):
        """
        """
        pass

    for wo in WidgetOrder.query.all():
        slug = slugify(wo.name, lowercase=True, separator="_")
        sf = SelectField(wo.name, choices=position_choices(),
                         validators=[prevent_identical],
                         render_kw={'class': 'form-control'})
        setattr(Form, slug, sf)

    return Form()


