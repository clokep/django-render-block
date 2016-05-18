from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context, RequestContext, TextNode


class BlockNotFound(Exception):
    """The expected block was not found."""


def _render_template_block(template, block_name, context):
    """
    Renders a single block from a template. This template should have previously
    been rendered.
    """
    template._render(context)
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
            if hasattr(node, key):
                try:
                    return _render_template_block_nodelist(getattr(node, key), block_name, context)
                except:
                    pass

    # The wanted block was not found in this template, attempt to find it in any
    # templates this inherits from.
    for node in nodelist:
        if isinstance(node, ExtendsNode):
            try:
                return _render_template_block(node.get_parent(context), block_name, context)
            except BlockNotFound:
                pass

    # The wanted block_name was not found.
    raise BlockNotFound


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

    return _render_template_block(t, block_name, context_instance)
