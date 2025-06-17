from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ''
    

@register.filter
def progress(user_points, required_points):
    try:
        percent = (int(user_points) / int(required_points)) * 100
        return round(min(percent, 100))  # Cap at 100%
    except (ValueError, ZeroDivisionError, TypeError):
        return 0