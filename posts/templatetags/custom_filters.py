from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def time_ago_with_timestamp(value):
    now = timezone.now()
    diff = now - value
    
    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    months = days // 30
    years = days // 365
    
    if years > 0:
        time_ago = f"{int(years)} year{'s' if years != 1 else ''} ago"
    elif months > 0:
        time_ago = f"{int(months)} month{'s' if months != 1 else ''} ago"
    elif days > 0:
        time_ago = f"{int(days)} day{'s' if days != 1 else ''} ago"
    elif hours > 0:
        time_ago = f"{int(hours)} hour{'s' if hours != 1 else ''} ago"
    elif minutes > 0:
        time_ago = f"{int(minutes)} minute{'s' if minutes != 1 else ''} ago"
    else:
        time_ago = "just now"
    
    timestamp = value.strftime("%Y-%m-%d %H:%M:%S UTC")
    return f'<span title="{timestamp}">{time_ago}</span>' 