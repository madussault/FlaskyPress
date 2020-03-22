"""Integrates global functions for use in our templates.
"""
from app.categories import bp
from app.models import Category, Post


@bp.app_template_global()
def categories_w_post_count():
    """Tells us how many blog entries were posted under each category.

    return
    ------
    dic : dictionary
        Contains categories names along with their post count.
    """
    dic = {}
    categories = Category.query.all()
    for c in categories:
        posts = (Post.query.join(Category.posts)
                 .filter(Category.id == c.id, Post.is_published == True).all())
        if posts:
            dic[c.name] = (c.slug, len(posts))
    post_count = Post.query.filter_by(categories=None, is_published=True,
                                      is_page=False).count()
    if post_count > 0:
        dic['uncategorized'] = ('uncategorized', post_count)
    return dic
