from django import template

register = template.Library()


@register.filter
def changePercent(value, arg):
    try:
        ans = round(((float(value)/float(arg))-1)*100,2)
        return round(ans,2)
    except (ZeroDivisionError, ValueError):
        return None
