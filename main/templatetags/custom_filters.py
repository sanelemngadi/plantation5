from django import template

register = template.Library()

@register.filter(name='shorten')
def shorten(value, arg):
    start, end = map(int, arg.split(':'))
    return value[start:end]
