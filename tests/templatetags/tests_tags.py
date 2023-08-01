from django import template
from django.template.base import Node

register = template.Library()


def none_nodelist(parser, token):
    node = Node()
    for attr in node.child_nodelists:
        setattr(node, attr, None)
    return node


register.tag("none_nodelist", none_nodelist)
