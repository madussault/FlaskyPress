from flask import render_template, request, flash
from flask_login import login_required
from app import db
from app.controls.forms import (SearchBarControlsForm, CategoriesControlsForm,
                                SocialsForm)
from app.models import (SearchBarControls, CategoriesControls, Social,
                        WidgetOrder)
from app.controls import bp
from app.controls.forms import widgets_order_form


@bp.route('/controls/search_bar', methods=['GET', 'POST'])
@login_required
def search_bar():
    """Allow the user to change the placement of the search bar in the layout.

    Three options are offered to the user:
    - To place the search bar in the sidebar.
    - To place the search bar in the top menu.
    - To disable search functionality and at the same time remove the search
     bar from the layout.
    """
    title = "Search Bar Configuration"
    sbc = SearchBarControls.query.first()
    form = SearchBarControlsForm()
    if form.validate_on_submit():
        sbc.placement = form.placement_field.data
        sbc.add_to_or_remove_from_sidebar()
        db.session.commit()
        flash('Configuration parameters successfully saved.',
              'success')
    elif request.method == 'GET':
        form.placement_field.data = sbc.placement
    return render_template('controls/search_bar.html', form=form, title=title)


@bp.route('/controls/categories', methods=['GET', 'POST'])
@login_required
def categories():
    """Allow the user to decide where in the layout categories should be
    displayed.

    Three options are offered to the user:
    - Display posts categories and listing all the blog categories in a
      sidebar widget.
    - Display posts categories only.
    - Display no categories at all. Will disable the use of categories in the
      blog.
    """
    title = "Categories Feature Configuration"
    c = CategoriesControls.query.first()
    form = CategoriesControlsForm()
    if form.validate_on_submit():
        c.presence = form.presence_field.data
        c.add_to_or_remove_from_sidebar()
        db.session.commit()
        flash('Configuration parameters successfully saved.',
              'success')
    elif request.method == 'GET':
        form.presence_field.data = c.presence
    return render_template('controls/categories.html', form=form, title=title)


@bp.route('/controls/socials', methods=['GET', 'POST'])
@login_required
def socials():
    """Allow the user to add his social address in the footer.
    """
    title = "Configure Socials"
    form = SocialsForm()
    social_entries = Social.query.all()
    if form.validate_on_submit():
        for s in social_entries:
            for field in form:
                if s.name in field.label.text:
                    s.address = field.data
        db.session.commit()
        flash('Your social addresses were successfully saved.',
              'success')
    elif request.method == 'GET':
        for s in social_entries:
            for field in form:
                if s.name in field.label.text:
                    field.data = s.address
    return render_template('controls/socials.html', form=form, title=title)


@bp.route('/controls/widgets_order', methods=['GET', 'POST'])
@login_required
def widgets_order():
    """Allow the user to re-order the widgets in the sidebar.
    """
    title = "Configure Sidebar Widgets Order"
    form = widgets_order_form()
    widgets_positions = WidgetOrder.query.all()
    if form.validate_on_submit():
        for wp in widgets_positions:
            for field in form:
                if wp.name == field.label.text:
                    wp.position = field.data
        db.session.commit()
        flash('Your choices were successfully saved.', 'success')
    elif request.method == 'GET':
        for wp in widgets_positions:
            for field in form:
                if wp.name == field.label.text:
                    field.default = wp.position
        form.process()
    return render_template('controls/widgets_order.html', form=form,
                           title=title, widgets_positions=widgets_positions)
