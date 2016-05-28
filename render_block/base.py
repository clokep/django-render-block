from __future__ import absolute_import

from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.template.backends.django import Template as DjangoTemplate
from django.template.base import TemplateSyntaxError


class BlockNotFound(TemplateSyntaxError):
    """The expected block was not found."""


class UnsupportedEngine(ImproperlyConfigured):
    """An engine that we cannot render blocks from was used."""


def render_block_to_string(template_name, block_name, context=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.

        template_name
            The name of the template to load and render. If it's a list of
            template names, Django uses select_template() instead of
            get_template() to find the template.
    """

    # Like render_to_string, template_name can be a string or a list/tuple.
    if isinstance(template_name, (tuple, list)):
        t = loader.select_template(template_name)
    else:
        t = loader.get_template(template_name)

    # Create the context instance.
    context = context or {}

    # The Django backend.
    if isinstance(t, DjangoTemplate):
        from render_block.django import django_render_block as render_template_block
        return render_template_block(t, block_name, context)
    else:
        raise UnsupportedEngine('Can only render blocks from the Django template backend.')
