from django.http import HttpResponse
from django.views import View

from render_block import render_block


class BlockView(View):
    """
    This view simply calls render_block with parameters from the data of the request.
    """

    def post(self, request) -> HttpResponse:
        context = {
            key: request.POST.get(key)
            for key in request.POST.keys()
            if key not in ("template_name", "block_name")
        }
        if context == {}:
            context = None

        return render_block(
            request,
            template_name=request.POST.get("template_name"),
            block_name=request.POST.get("block_name"),
            context=context,
            status=request.POST.get("status"),
        )
