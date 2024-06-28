from django import template

register = template.Library()


@register.simple_tag()
def raise_exception():
    raise Exception("Exception raised in template tag.")
