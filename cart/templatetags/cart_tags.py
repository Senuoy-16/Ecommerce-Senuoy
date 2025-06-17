from django import template

register = template.Library()

@register.filter
def get_item_quantity(cart, variation_id):
    item = cart.get(str(variation_id))
    return item.get('quantity') if item else 1