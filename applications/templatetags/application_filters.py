from django import template

register = template.Library()

@register.filter
def filter_by_status(applications, status):
    """Filter applications by their status."""
    return [app for app in applications if app.status == status] 