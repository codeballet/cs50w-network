from django import template

register = template.Library()


# define zip as a template filter
@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)
