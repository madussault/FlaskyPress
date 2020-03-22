"""Integrates global functions for use in our templates.
"""

from app.controls import bp
from app.models import (SearchBarControls, CategoriesControls,
                        WidgetOrder)


@bp.app_template_global()
def search_bar_placement():
    """Query the actual search bar placement from the db.

    return
    ------
    sbc.placement : str
        Name the choice of placement.
    """
    sbc = SearchBarControls.query.first()
    return sbc.placement


@bp.app_template_global()
def categories_presence():
    """Query from the db where in the layout the categories are displayed.

    return
    ------
    cc.presence : str
        Name where the categories should be displayed.
    """
    cc = CategoriesControls.query.first()
    return cc.presence


@bp.app_template_global()
def sidebar_widget_count():
    """Return the number of widgets placed in the sidebar.

    return
    ------
    WidgetOrder.query.count() : int
        Number representing the qty of widgets assigned to the sidebar.
    """
    return WidgetOrder.query.count()


@bp.app_template_global()
def ordered_widgets():
    """Returns a list of the widgets to display in the sidebar.

    Since it is a list the widget titles/names are ordered. The order
    correspond to the position each of them were assigned in the sidebar.

    return
    ------
    widgets : list
        Contains names of the widgets assigned to the sidebar and ordered
        according to our need.
    """
    wo = WidgetOrder.query
    widgets_count = wo.count()
    widgets = []
    num = 0
    for i in range(widgets_count):
        num += 1
        for w in wo.all():
            if w.position == str(num):
                widgets.append(w.name)
    return widgets


