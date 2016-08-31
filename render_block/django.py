from __future__ import absolute_import

from django.template import Context
from django.template.base import TextNode
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
        # Before trying to render the template, we need to traverse the tree of
        # parent templates and find all blocks in them.
        _build_block_context(template, context_instance)

        return _render_template_block(template, block_name, context_instance)


def _build_block_context(template, context):
    """Populate the block context with BlockNodes from parent templates."""

    # Ensure there's a BlockContext before rendering. This allows blocks in
    # ExtendsNodes to be found by sub-templates (allowing {{ block.super }} and
    # overriding sub-blocks to work).
    if BLOCK_CONTEXT_KEY not in context.render_context:
        context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
    block_context = context.render_context[BLOCK_CONTEXT_KEY]

    for node in template.nodelist:
        if isinstance(node, ExtendsNode):
            compiled_parent = node.get_parent(context)

            # Add the parent node's blocks to the context. (This ends up being
            # similar logic to ExtendsNode.render(), where we're adding the
            # parent's blocks to the context so a child can find them.)
            block_context.add_blocks(
                {n.name: n for n in compiled_parent.nodelist.get_nodes_by_type(BlockNode)})

            _build_block_context(compiled_parent, context)
            return

        # The ExtendsNode has to be the first non-text node.
        if isinstance(node, TextNode):
            break


def _render_template_block(template, block_name, context):
    """Renders a single block from a template."""
    return _render_template_block_nodelist(template.nodelist, block_name, context)


def _render_template_block_nodelist(nodelist, block_name, context):
    """Recursively iterate over a node to find the wanted block."""

    # An ExtendsNode, if necessary.
    extends_node = None

    # This is guaranteeded to exist from above.
    block_context = context.render_context[BLOCK_CONTEXT_KEY]

    # Attempt to find the wanted block in the current template.
    for node in nodelist:
        # ExtendsNode must be the first non-TextNode, so this check is quickly
        # gratuitous.
        if isinstance(node, ExtendsNode):
            # Save the parent template in case the only instance of this block
            # is from the super-template. (We don't know this until we traverse
            # the rest of the nodelist, unfortunately.)
            extends_node = node

        # If the wanted block was found, return it.
        if isinstance(node, BlockNode):
            # No matter what, add this block to the rendering context.
            block_context.push(node.name, node)

            # If the name matches, you're all set and we found the block!
            if node.name == block_name:
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

    # If the node was not found in this template, but there is an ExtendsNode,
    # check it for the wanted block.
    if extends_node:
        return _render_template_block(node.get_parent(context), block_name, context)

    # The wanted block_name was not found.
    raise BlockNotFound("block with name '%s' does not exist" % block_name)
