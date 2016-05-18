from django.template.base import TemplateSyntaxError
from django.template import loader, Context
from django.template.loader_tags import BlockNode, ExtendsNode


class BlockNotFound(TemplateSyntaxError):
    """The expected block was not found."""


def _render_template_block(template, block_name, context):
    """Renders a single block from a template."""
    return _render_template_block_nodelist(template.nodelist, block_name, context)


def _render_template_block_nodelist(nodelist, block_name, context):
    """Recursively iterate over a node to find the wanted block."""

    # Attempt to find the wanted block in the current template.
    for node in nodelist:
        # If the wanted block was found, return it.
        if isinstance(node, BlockNode) and node.name == block_name:
            return node.render(context)

        # If a node has children, recurse into them.
        for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
            # Try to get the recursive property, if it exists.
            try:
                new_node = getattr(node, key)
            except AttributeError:
                continue

            # Try to find the block recursively.
            try:
                return _render_template_block_nodelist(new_node, block_name, context)
            except BlockNotFound:
                continue

    # The wanted block was not found in this template, attempt to find it in any
    # templates this inherits from.
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                return _render_template_block(node.get_parent(context), block_name, context)
            except BlockNotFound:
                pass

    # The wanted block_name was not found.
    raise BlockNotFound("block with name '%s' does not exist" % block_name)


def render_block_to_string(template_name, block_name, context=None, context_instance=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.

        template_name
            The name of the template to load and render. If it?s a list of
            template names, Django uses select_template() instead of
            get_template() to find the template.
    """

    context = context or {}

    # Like render_to_string, template_name can be a string or a list/tuple.
    if isinstance(template_name, (tuple, list)):
        t = loader.select_template(template_name)
    else:
        t = loader.get_template(template_name)

    if context_instance:
        context_instance.update(context)
    else:
        context_instance = Context(context)

    # TODO This only works with the Django backend currently.
    t = t.template

    # Bind the template to the context.
    with context_instance.bind_template(t):
        return _render_template_block(t, block_name, context_instance)
