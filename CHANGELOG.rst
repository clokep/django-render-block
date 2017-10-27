.. :changelog:

Changelog
#########

next (xxx xx, xxxx)
===================

*   Officially support Django 1.11 and Django 2.0.

0.5 (September 1, 2016)
=======================

*   Fixes a major issue with inheriting templates and rendering a block found in
    the parent template, but overwriting part of it in the child template.
    (`#8 <https://github.com/clokep/django-render-block/pull/8>`_)

0.4 (August 4, 2016)
====================

*   Initial support for using the `Jinja2 <http://jinja.pocoo.org/>`_ templating
    engine. See README for caveats. (`#3 <https://github.com/clokep/django-render-block/pull/3>`_)
*   Support Django 1.10. (`#5 <https://github.com/clokep/django-render-block/pull/5>`_)
*   Support Python 3. (`#6 <https://github.com/clokep/django-render-block/pull/6>`_)

0.3.1 (June 1, 2016)
====================

*   Refactoring to make more generic (for potentially supporting multiple
    templating engines).

0.3 (May 27, 2016)
==================

*   Largely rewritten.
*   Updated to support modern Django (1.8, 1.9):

    *   Guards against different template backends.
    *   Uses internal APIs for each node.
    *   Removed ``context_instance`` parameter.
    *   Support for calling ``{{ block.super }}``.

0.2.2 (January 10, 2011)
========================

*   Updated per
    `comment 3466 on Django Snippet 942 <https://djangosnippets.org/snippets/942/#c3466>`_
    to fix an issue with nested extends. The specific bug was not reproducible,
    but the additional code shouldn't hurt.

0.2.1 (August 27, 2010)
=======================

*   Updated per
    `comment 3237 on Django Snippet 942 <https://djangosnippets.org/snippets/942/#c3237>`_
    to remove a pointless render. The specific bug was not reproducible, but the
    code is extraneous.

0.2 (August 4, 2008)
====================

*   Updated version from
    `Django Snippet 942 <https://djangosnippets.org/snippets/942/>`_ by zbyte64.
*   Improves include:

    1.  Simpler/better handling of "extends" block tag
    2.  Searches If/Else blocks
    3.  Less code
    4.  Allow list of templates to be passed which is closer to the behavior of
        render_to_response


0.1 (May 22, 2008)
==================

*   Initial version from
    `Django Snippet 769 <https://djangosnippets.org/snippets/769/>`_ by sciyoshi.
*   Supports Django 0.96.
