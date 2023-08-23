from django import template

import time


register = template.Library()


@register.filter(name='relative_timestamp')
def relative_timestamp(unix_timestamp):
    current_time = time.time()

    time_diff = int(current_time - unix_timestamp)

    if time_diff < 60:
        return f"{time_diff} seconds ago"
    elif time_diff < 3600:
        minutes = time_diff // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif time_diff < 86400:
        hours = time_diff // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif time_diff < 2620800:
        days = time_diff // 86400
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif time_diff < 31449600:
        months = time_diff // 2620800
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = time_diff // 31449600
        return f"{years} year{'s' if years != 1 else ''} ago"