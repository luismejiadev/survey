"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'survey.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'survey.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class ChartDashboard(modules.DashboardModule):
    """
    """
    template = 'admin/dashboard/chart_dashboard.html'
    layout = 'stacked'
    headers = []
    fields = []
    children = []

    def __init__(self, title, chart_id, **kwargs):
        super(ChartDashboard, self).__init__(title, **kwargs)
        self.chart_id=chart_id
        self.title = title

    def init_with_context(self, context):
        from surveys.utils import get_last_survey
        context['object'] = get_last_survey()
        return super(ChartDashboard, self).init_with_context(context)


class TableDashboard(modules.DashboardModule):
    """
    """
    template = 'admin/dashboard/table_dashboard.html'
    layout = 'stacked'
    headers = []
    fields = []

    def __init__(self, title, children, headers, fields, **kwargs):
        super(TableDashboard, self).__init__(title, **kwargs)
        self.children = children or []
        self.headers = headers
        self.fields = fields
        self.title = title


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for survey.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Results'),
            children=[
                {
                    'title': _('Results'),
                    'url': reverse('survey_list'),
                    'external': False,
                }
            ]
        ))

        from surveys.utils import get_last_survey
        survey = get_last_survey()
        self.children.append(
            TableDashboard(
                title='Last Survey Top Questions',
                children = survey.top_questions,
                headers = ['Plulication Date', 'Code', 'Question', 'Total Count'],
                fields = [
                    'pub_date',
                    'slug',
                    'question_text',
                    'user_choices_count'
                ]
            )
        )
        self.children.append(
            ChartDashboard(
                title='Survey Chart',
                chart_id=1,
                childrens=[]
                )
        )
