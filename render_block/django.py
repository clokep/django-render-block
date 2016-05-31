from __future__ import absolute_import

from django.template import Context
from django.template.loader_tags import (BLOCK_CONTEXT_KEY,
                                         BlockContext,
                                         BlockNode,
                                         ExtendsNode)

from render_block.exceptions import BlockNotFound


def django_render_block(template, block_name, context):
    # Create a Django Context.
    context_instance = Context(context)

    # Get the underlying django.template.base.Template object.
    template = template.template

    # Bind the template to the context.
    with context_instance.bind_template(template):
        return _render_template_block(template, block_name, context_instance)


def _render_template_block(template, block_name, context):
    """Renders a single block from a template."""
    return _render_template_block_nodelist(template.nodelist, block_name, context)


def _render_template_block_nodelist(nodelist, block_name, context):
    """Recursively iterate over a node to find the wanted block."""

    # The result, if found via an ExtendsNode.
    rendered_extends_block = None

    # Attempt to find the wanted block in the current template.
    for node in nodelist:
        # ExtendsNode must be first, so this check is gratuitous after the first
        # iteration.
        if isinstance(node, ExtendsNode):
            # Attempt to render this block in the parent, save it in case the
            # only instance of this block is from the super-template. (We don't
            # know this until we traverse the rest of the nodelist,
            # unfortunately.)
            try:
                rendered_extends_block = _render_template_block(node.get_parent(context), block_name, context)
            except BlockNotFound:
                pass

        # If the wanted block was found, return it.
        if isinstance(node, BlockNode) and node.name == block_name:
            # Ensure there's a BlockContext before rendinering. This allows
            # blocks in ExtendsNodes to be found by sub-templates (essentially,
            # allowing {{ block.super }} to work.
            if BLOCK_CONTEXT_KEY not in context.render_context:
                context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
            context.render_context[BLOCK_CONTEXT_KEY].push(block_name, node)

            return node.render(context)

        # If a node has children, recurse into them. Based on
        # django.template.base.Node.get_nodes_by_type.
        for attr in node.child_nodelists:
            try:
                new_nodelist = getattr(node, attr)
            except AttributeError:
                continue

            # Try to find the block recursively.
            try:
                return _render_template_block_nodelist(new_nodelist, block_name, context)
            except BlockNotFound:
                continue

    # No better node was found besides the one from an ExtendsNode. Return it!
    if rendered_extends_block:
        return rendered_extends_block

    # The wanted block_name was not found.
    raise BlockNotFound("block with name '%s' does not exist" % block_name)
