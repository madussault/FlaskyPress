from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.content_widgets.forms import ContentWidgetForm
from app.models import ContentWidget
from app.content_widgets import bp
from sqlalchemy import exc


@bp.route('/content_widgets')
@login_required
def index():
    """List our sidebar content widgets.
    """
    title = 'Content Widgets'
    published_cw = (ContentWidget.query.filter_by(is_published=True)
                    .order_by(ContentWidget.title)
                    .all())
    draft_cw = (ContentWidget.query.filter_by(is_published=False)
                .order_by(ContentWidget.title)
                .all())
    return render_template('content_widgets/index.html',
                           published_content_widgets=published_cw,
                           draft_content_widgets=draft_cw,
                           title=title)


@bp.route('/create_content_widget', methods=['GET', 'POST'])
@login_required
def create():
    """For creating new sidebar content widgets.
    """
    title = 'New Content Widget'
    form = ContentWidgetForm()
    if form.validate_on_submit():
        cw = ContentWidget(title=form.title_field.data,
                           content=form.content_field.data,
                           is_published=form.publish.data
                           )
        cw.slugify_title()
        try:
            db.session.add(cw)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash('Error: This title is already in use.', 'danger')
        else:
            cw.add_to_or_remove_from_sidebar()
            if cw.is_published:
                flash('Widget is now displaying is the sidebar.', 'success')
            else:
                flash('Widget saved for later publishing.', 'success')
            return redirect(url_for('content_widgets.index'))
    return render_template('content_widgets/create.html', form=form,
                           title=title)


@bp.route('<slug>/edit_content_widget', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """For editing existing sidebar content widgets.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular content
        widget on our blog in an easy to read form.
    """
    title = 'Edit Content Widget'
    cw = ContentWidget.query.filter_by(slug=slug).first_or_404()
    original_title = cw.title
    form = ContentWidgetForm()
    if form.validate_on_submit():
        cw.title = form.title_field.data
        cw.content = form.content_field.data
        cw.is_published = form.publish.data
        cw.is_page = True
        cw.slugify_title()
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash('Error: This title is already in use.', 'danger')
        else:
            cw.add_to_or_remove_from_sidebar()
            cw.remove_invalid_title_from_sidebar(original_title)
            if cw.is_published:
                flash('Widget successfully edited and published.', 'success')
            else:
                flash('Widget saved for later publishing.', 'success')
            return redirect(url_for('content_widgets.index'))
    elif request.method == 'GET':
        form.title_field.data = cw.title
        form.content_field.data = cw.content
        form.publish.data = cw.is_published
    return render_template('content_widgets/create.html', form=form, title=title,
                           content_widget=cw)


@bp.route('/<slug>/delete_content_widget', methods=['GET', 'POST'])
@login_required
def delete(slug):
    """For deleting sidebar content widgets.
    """
    title = 'Delete Content Widget'
    cw = ContentWidget.query.filter_by(slug=slug)
    if request.method == 'POST':
        first_cw = cw.first()
        first_cw.remove_from_sidebar()
        cw.delete()
        db.session.commit()
        flash('Content widget deleted.', 'success')
        return redirect(url_for('content_widgets.index'))
    return render_template('content_widgets/delete.html',
                           content_widget=cw.first_or_404(), title=title)

