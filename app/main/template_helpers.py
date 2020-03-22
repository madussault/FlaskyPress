"""Integrates global functions and filters for use in our templates.
"""

from app.main import bp
from app.models import Post, Social
import re


@bp.app_template_global()
def draft_exists():
    """Query the db to find if any draft post exist.
    """
    return Post.query.filter_by(is_published=False, is_page=False).first()


@bp.app_template_global()
def get_socials():
    """Get the name and the address of the social account entered at
    ``/controls/socials``.

    return
    ------
    socials : dictionary
        Contains the names of the services and their addresses.
    """
    socials = {}
    social_entries = Social.query.all()
    for s in social_entries:
        if s.address != '':
            socials[s.name] = s.address
    return socials


@bp.app_template_filter()
def read_more(html, anchor):
    """Will truncate the text at the place the user left a [read_more] tag.

    This truncation will appear in the /index, /drafts and /search pages.
    The purpose is to make the listing of posts more brief.

    Parameters
    ----------
    html : class 'markupsafe.Markup'
        Html of the posts.
    anchor : class 'markupsafe.Markup'
        Anchor tag linking to the post detail.

    Returns
    -------
    f'{splitted_html[0]}{anchor}' : str
        Returns the html of the truncated post including the hyperlink
        leading to the detail of the post in full.
    html : class 'markupsafe.Markup'
        Returns the html of the post in full. Happens when no [read_more] tag
        is found.
    """
    splitted_html = re.split('\[read_more\]', html, maxsplit=1)
    if len(splitted_html) > 1:
        return f'{splitted_html[0]}{anchor}'
    return html


@bp.app_template_filter()
def remove_read_more(html):
    """Will remove the [read_more] tag from the detail of a post.

    Parameters
    ----------
    html : class 'markupsafe.Markup'
        Html of the posts.

    Returns
    -------
    splitted_html[0] + splitted_html[1] : str
        Returns the html of the post after having removed the [read_more] tag.
    html : class 'markupsafe.Markup'
        Returns the html of the post without doing any operation on it.
        Happens when no [read_more] tag is found.
    """
    splitted_html = re.split('\[read_more\]', html, maxsplit=1)
    if len(splitted_html) > 1:
        return splitted_html[0] + splitted_html[1]
    return html
