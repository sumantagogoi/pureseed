from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    if value and arg:
        return '{:.2f}'.format(round((float(value) * float(arg)),1))
    else:
        return ""


@register.filter
def number2Dec(value):
    if value:
        return '{:.2f}'.format(round((float(value) * float(arg)),1))
    else:
        return ""

@register.filter
def pk(value):
    return value._id