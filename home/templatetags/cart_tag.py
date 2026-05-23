# Source - https://stackoverflow.com/a/62938087
# Posted by Harben, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-23, License - CC BY-SA 4.0

from django import template    

register = template.Library()

@register.filter(name='cart_quantity')
def cart_quantity(product  , cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
             return cart.get(id)
    return 0

# Multiply filter for template usage
@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
