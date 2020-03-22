from flask import (render_template, flash, redirect, url_for, request, session)
from flask_login import login_required
from app import db
from app.pages.forms import PageForm
from app.models import Post
from app.pages import bp
from sqlalchemy import exc
from datetime import datetime


@bp.route('/pages')
@login_required
def index():
    """List all the pages we created.
    """
    title = 'Page Index'
    published_pages = (Post.query.filter_by(is_page=True, is_published=True)
                       .order_by(Post.timestamp.desc())).all()
    draft_pages = (Post.query.filter_by(is_page=True, is_published=False)
                   .order_by(Post.timestamp.desc())).all()
    return render_template('pages/index.html', published_pages=published_pages,
                           draft_pages=draft_pages,
                           title=title)


@bp.route('/create_page', methods=['GET', 'POST'])
@login_required
def create():
    """For creating new pages.
    """
    title = 'New Page'
    form = PageForm()
    if form.validate_on_submit():
        page = Post(title=form.title_field.data,
                    content=form.content_field.data,
                    is_published=form.publish.data,
                    is_page=True)
        page.slugify_title()
        if form.preview.data:
            page.timestamp = datetime.utcnow()
            session['post'] = page
            return redirect(url_for('main.preview', slug=page.slug))
        else:
            try:
                db.session.add(page)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash('Error: This title is already in use.', 'danger')
            else:
                if page.is_published:
                    flash('Page is now live.', 'success')
                else:
                    flash('Page saved for later publishing.', 'success')
                return redirect(url_for('pages.index'))
    return render_template('pages/create.html', form=form, title=title)


@bp.route('<slug>/edit_page', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """Used to edit a particular page.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular page
        on our blog in an easy to read form.
    """
    title = 'Edit Page'
    page = Post.query.filter_by(slug=slug, is_page=True).first_or_404()
    form = PageForm()
    if form.validate_on_submit():
        page.title = form.title_field.data
        page.content = form.content_field.data
        page.is_published = form.publish.data
        page.is_page = True
        page.slugify_title()
        if form.preview.data:
            session['post'] = page
            return redirect(url_for('main.preview', slug=page.slug))
        else:
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash('Error: This title is already in use.', 'danger')
            else:
                if page.is_published:
                    flash('Page successfully edited and published.', 'success')
                else:
                    flash('Page saved for later publishing.', 'success')
                return redirect(url_for('pages.index'))
    elif request.method == 'GET':
        form.title_field.data = page.title
        form.content_field.data = page.content
        form.publish.data = page.is_published
    return render_template('pages/create.html', form=form, title=title,
                           page=page)


@bp.route('/<slug>/delete_page', methods=['GET', 'POST'])
@login_required
def delete(slug):
    """When we want to delete a particular page.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular page
        on our blog in an easy to read form.
    """
    title = 'Delete Page'
    page = Post.query.filter_by(slug=slug, is_page=True)
    if request.method == 'POST':
        page.delete()
        db.session.commit()
        flash('Page deleted.', 'success')
        return redirect(url_for('pages.index'))
    return render_template('pages/delete.html', page=page.first_or_404(),
                           title=title)

