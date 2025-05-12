from typing import NoReturn

from django import template

register = template.Library()


@register.simple_tag()
def raise_exception() -> NoReturn:
    raise Exception("Exception raised in template tag.")
