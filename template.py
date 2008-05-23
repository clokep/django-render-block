# file template.py

import new
from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context, RequestContext, TextNode

class BlockNotFound(Exception):
    pass

class ExtendsNodeMixin(object):
    def compile(self, context):
        """
        Compiles this node and returns the compiled parent.
        """
        compiled_parent = self.get_parent(context)
        pos = 0
        while isinstance(compiled_parent.nodelist[pos], TextNode):
            pos += 1
        parent_is_child = isinstance(compiled_parent.nodelist[pos], ExtendsNode)
        parent_blocks = dict([(n.name, n) for n in compiled_parent.nodelist.get_nodes_by_type(BlockNode)])
        for block_node in self.nodelist.get_nodes_by_type(BlockNode):
            # Check for a BlockNode with this node's name, and replace it if found.
            try:
                parent_block = parent_blocks[block_node.name]
            except KeyError:
                # This BlockNode wasn't found in the parent template, but the
                # parent block might be defined in the parent's *parent*, so we
                # add this BlockNode to the parent's ExtendsNode nodelist, so
                # it'll be checked when the parent node's render() is called.
                if parent_is_child:
                    compiled_parent.nodelist[pos].nodelist.append(block_node)
            else:
                # Keep any existing parents and add a new one. Used by BlockNode.
                parent_block.parent = block_node.parent
                parent_block.add_parent(parent_block.nodelist)
                parent_block.nodelist = block_node.nodelist
        return compiled_parent

ExtendsNode.__bases__ += (ExtendsNodeMixin,)

def render(self, context):
    self.compiled_parent = self.compile(context)
    return self.compiled_parent.render(context)

ExtendsNode.render = new.instancemethod(render, None, ExtendsNode)

def render_template_block(template, block, context):
    """
    Renders a single block from a template. This template should have previously been rendered.
    """
    if len(template.nodelist) and not isinstance(template.nodelist[0], ExtendsNode):
        for blk in template.nodelist:
            if isinstance(blk, BlockNode) and blk.name == block:
                return blk.render(context)
        raise BlockNotFound
    for blk in template.nodelist[0].nodelist:
        if isinstance(blk, BlockNode) and blk.name == block:
            return blk.render(context)
    return render_template_block(template.nodelist[0].compiled_parent, block, context)

def render_block_to_string(template_name, block, dictionary=None, context_instance=None):
    """
    Loads the given template_name and renders the given block with the given dictionary as
    context. Returns a string.
    """
    dictionary = dictionary or {}
    t = loader.get_template(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)
    t.render(context_instance)
    return render_template_block(t, block, context_instance)

def direct_block_to_template(request, template, block, extra_context=None, mimetype=None, **kwargs):
    """
    Render a given block in a given template with any extra URL parameters in the context as
    ``{{ params }}``.
    """
    if extra_context is None:
    	extra_context = {}
    dictionary = {'params': kwargs}
    for key, value in extra_context.items():
        if callable(value):
            dictionary[key] = value()
        else:
            dictionary[key] = value
    c = RequestContext(request, dictionary)
    t = loader.get_template(template)
    t.render(c)
    return HttpResponse(render_template_block(t, block, c), mimetype=mimetype)
