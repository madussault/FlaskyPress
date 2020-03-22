from flask import (render_template, flash, redirect, url_for, request,
                   current_app, make_response, session, abort)
from flask_login import login_required, current_user
from app import db
from app.main.forms import PostForm
from app.models import Post, SearchBarControls
from app.main import bp
from sqlalchemy import exc
from datetime import datetime
from app.categories.utils import (set_categories, del_unused_categories,
                                  disassociate_categories)


@bp.route('/')
@bp.route('/index')
def index():
    """The Homepage. Published posts are listed here by date.
    """
    title = 'Home'
    page = request.args.get('page', 1, type=int)
    posts = (Post.query.filter_by(is_published=True, is_page=False)
             .order_by(Post.timestamp.desc())
             .paginate(page, current_app.config['POSTS_PER_PAGE'], False))
    next_url = url_for('main.index',
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index',
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', posts=posts.items,
                           title=title, next_url=next_url, prev_url=prev_url)


@bp.route('/drafts')
@login_required
def drafts():
    """Posts saved as drafts are listed here by date.
    """
    title = 'Drafts'
    page = request.args.get('page', 1, type=int)
    posts = (Post.query.filter_by(is_published=False, is_page=False)
             .order_by(Post.timestamp.desc())
             .paginate(page, current_app.config['POSTS_PER_PAGE'], False))
    next_url = url_for('main.drafts',
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.drafts',
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', posts=posts.items,
                           title=title, next_url=next_url, prev_url=prev_url)


@bp.route('/search')
def search():
    """Display search results.

    This route becomes disabled if the admin decides to remove the search bar
    from the site interface.
    """
    if SearchBarControls.query.filter_by(placement='no_search').first():
        abort(404)
    title = 'Search'
    search_query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    try:
        posts = (Post.query.whooshee_search(search_query,
                                            match_substrings=False)
                 .filter_by(is_published=True)
                 .paginate(page, current_app.config['POSTS_PER_PAGE'], False))
    except ValueError:
        flash('Search string must have at least 3 characters.', 'warning')
        return redirect(url_for('main.index'))
    if not posts.items:
        flash('Sorry, your search query did not return any results.', 'info')
    next_url = url_for('main.search', page=posts.next_num,
                       q=search_query) if posts.has_next else None
    prev_url = url_for('main.search', page=posts.prev_num,
                       q=search_query) if posts.has_prev else None
    return render_template('index.html', posts=posts.items,
                           title=title, next_url=next_url, prev_url=prev_url)


@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create():
    """We create new posts using this route.

    If the checkbox labeled ``Publish Now`` is ticked at the moment of
    posting the form the post will be published. Else it's going to be saved
    as a draft.
    """
    title = 'New Post'
    form = PostForm()
    if form.validate_on_submit():
        categories = set_categories(form.categories_field.data)
        post = Post(title=form.title_field.data,
                    content=form.content_field.data,
                    is_published=form.publish.data,
                    is_page=False,
                    categories=categories)
        post.slugify_title()
        if request.form.get('preview'):
            post.timestamp = datetime.utcnow()
            session['post'] = post
            return redirect(url_for('main.preview', slug=post.slug))
        else:
            try:
                db.session.add(post)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash('Error: This title is already in use.', 'danger')
            else:
                if post.is_published:
                    flash('Post is now live.', 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash('Post saved as draft.', 'success')
                    return redirect(url_for('main.drafts'))
    return render_template('create.html', form=form, title=title)


@bp.route('/sitemap.xml')
@bp.route('/sitemap')
def sitemap():
    """Display the sitemap.
    """
    posts = Post.query.filter_by(is_published=True).all()
    template = render_template('sitemap.xml', posts=posts)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


# The slug route must be placed after all the other routes, or else their
# respective names will be misinterpreted as slugs. For example in
# http://127.0.0.1:5000/create 'create' would be seen as a slug.
@bp.route('/<slug>')
def detail(slug):
    """This route show a post in full, whether it is a draft or a post.

    Logged in user can see drafts but the others can only see published posts.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular post
        on our blog in an easy to read form.
    """
    if current_user.is_authenticated:
        post = Post.query.filter_by(slug=slug).first_or_404()
    else:
        post = Post.query.filter_by(is_published=True,
                                    slug=slug).first_or_404()
    title = post.title
    return render_template('detail.html', post=post, title=title)


@bp.route('/<slug>/edit_post', methods=['GET', 'POST'])
@login_required
def edit(slug):
    """ Used to edit a particular post.

    If the checkbox labeled ``Publish Now`` is ticked at the moment of
    posting the form the post will be published. Else it's going to be saved
    as a draft.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular post
        on our blog in an easy to read form.
    """
    title = 'Edit Post'
    post = Post.query.filter_by(slug=slug, is_page=False).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        categories = set_categories(form.categories_field.data)
        post.title = form.title_field.data
        post.content = form.content_field.data
        post.is_published = form.publish.data
        post.is_page = False
        post.categories = categories
        post.slugify_title()
        if request.form.get('preview'):
            session['post'] = post
            session['categories'] = categories
            return redirect(url_for('main.preview', slug=post.slug))
        else:
            try:
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                flash('Error: This title is already in use.', 'danger')
            else:
                del_unused_categories()
                if post.is_published:
                    flash('Post successfully edited and published.', 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash('Post successfully edited and saved as draft.',
                          'success')
                    return redirect(url_for('main.drafts'))
    elif request.method == 'GET':
        form.title_field.data = post.title
        form.content_field.data = post.content
        form.publish.data = post.is_published
        for i in range(len(post.categories.all())):
            form.categories_field.entries[i].data = post.categories[i].name
    return render_template('create.html', form=form, title=title, post=post)


@bp.route('/<slug>/preview')
@login_required
def preview(slug):
    """Show the preview of a newly created or edited post.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular post
        on our blog in an easy to read form.
    """
    post = session['post']
    # When I put the post object for the edit route in a session I am not
    # capable to retrieve the categories from the stored post object.
    # `post.categories.all()` returns an empty list. So I decided to create a
    # separate session key containing the categories.
    if 'categories' in session:
        post.categories = session['categories']
        session['categories'] = ''
    title = f'Preview of "{post.title}"'
    return render_template('detail.html', post=post, title=title)


@bp.route('/<slug>/delete_post', methods=['GET', 'POST'])
@login_required
def delete(slug):
    """When we want to delete a particular post.

    Parameters
    ----------
    slug : str
        The slug is the part of the URL which identifies a particular post
        on our blog in an easy to read form.
    """
    title = 'Delete Post'
    p = Post.query.filter_by(slug=slug, is_page=False)
    if request.method == 'POST':
        disassociate_categories(p)
        p.delete()
        db.session.commit()
        del_unused_categories()
        flash('Post deleted.', 'success')
        return redirect(url_for('main.index'))
    return render_template('delete.html', post=p.first_or_404(), title=title)


