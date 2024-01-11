from django import template
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter(name='time_since')
def timesince_short(value):
    now = timezone.now()
    diff = now - value

    if diff < timedelta(minutes=1):
        return f"{diff.seconds}s"
    if diff < timedelta(hours=1):
        return f"{diff.seconds // 60}m"
    if diff < timedelta(days=1):
        return f"{diff.seconds // 3600}h"
    if diff < timedelta(weeks=1):
        return f"{diff.days}d"
    return f"{diff.days // 7}w"
