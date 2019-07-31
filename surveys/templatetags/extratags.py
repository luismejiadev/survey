from django import template
register = template.Library()

@register.filter
def get_value(obj,field):
    """gets value from Object or Dict. Supports ORM notation obj__field
    """
    if field is None or obj is None:
        return ''
    try:
        objects = field.split('__')
        if len(objects) > 1:
            row = obj
            for r in objects:
                value = getattr(row, r)
                row = value
        else:
            value = getattr(obj, field)

        return value
    except AttributeError:
        try:
            return obj[field]
        except:
            return ''
    except:
        return ''


tag_func = register.inclusion_tag('admin_tools/dashboard/dummy.html', takes_context=True)
def admin_tools_render_dashboard(context, location='index', dashboard=None):
    """render Admin Tools dashboard with Chats
    """
    from admin_tools.dashboard.models import DashboardPreferences
    from admin_tools.utils import get_media_url, get_admin_site_name
    from django.core.urlresolvers import reverse

    if dashboard is None:
        from settings.admin.dashboard import MonitorIndexDashboard
        dashboard = MonitorIndexDashboard()

    dashboard.init_with_context(context)
    dashboard._prepare_children()

    try:
        preferences = DashboardPreferences.objects.get(
            user=context['request'].user,
            dashboard_id=dashboard.get_id()
        ).data
    except DashboardPreferences.DoesNotExist:
        preferences = '{}'
        DashboardPreferences(
            user=context['request'].user,
            dashboard_id=dashboard.get_id(),
            data=preferences
        ).save()

    context.update({
        'template': dashboard.template,
        'dashboard': dashboard,
        'dashboard_preferences': preferences,
        'split_at': math.ceil(float(len(dashboard.children))/float(dashboard.columns)),
        'media_url': get_media_url(),
        'has_disabled_modules': len([m for m in dashboard.children \
                                if not m.enabled]) > 0,
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
admin_tools_render_dashboard = tag_func(admin_tools_render_dashboard)