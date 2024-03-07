from django import template

register = template.Library()

# @register.filter(name='in_list')
# def in_list(value, arg):
#     return value in arg

@register.filter(name='in_list')
def in_list(value, arg):
    arg_list = arg.split(',')
    return value in arg_list