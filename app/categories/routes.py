from flask import render_template, request, url_for, current_app, abort
from app.categories import bp
from app.models import Category, Post, CategoriesControls


@bp.route('/<slug>/category')
def index(slug):
    """The route a user go to see all blog entries posted under a certain
    category.
    """
    if CategoriesControls.query.filter_by(presence='no_categories').first():
        abort(404)
    page = request.args.get('page', 1, type=int)
    if slug == 'uncategorized':
        category_slug = slug
        title = "Category: uncategorized"
        posts = (Post.query
                 .filter_by(categories=None, is_published=True, is_page=False)
                 .order_by(Post.timestamp.desc())
                 .paginate(page, current_app.config['POSTS_PER_PAGE'], False))
    else:
        c = Category.query.filter_by(slug=slug).first_or_404()
        category_slug = c.slug
        title = f"Category: {c.name}"
        posts = (Post.query.join(Category.posts)
                 .filter(Category.id == c.id, Post.is_published == True)
                 .order_by(Post.timestamp.desc())
                 .paginate(page, current_app.config['POSTS_PER_PAGE'], False))
    next_url = url_for('categories.index', slug=slug,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('categories.index', slug=slug,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', posts=posts.items, title=title,
                           next_url=next_url, prev_url=prev_url,
                           category_slug=category_slug)


