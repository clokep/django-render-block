.. :changelog:

Changelog
#########

0.9 (December 14, 2021)
=======================

* Drop support for Django 3.0. (`#31 <https://github.com/clokep/django-render-block/pull/31>`_)
* Support Django 3.2 and 4.0. (`#27 <https://github.com/clokep/django-render-block/pull/27>`_,
  `#31 <https://github.com/clokep/django-render-block/pull/31>`_)
* Switch continuous integration to GitHub Actions. (`#26 <https://github.com/clokep/django-render-block/pull/26>`_,
  `#28 <https://github.com/clokep/django-render-block/pull/28>`_)
* Changed packaging to use setuptools declarative config in ``setup.cfg``.
  (`#32 <https://github.com/clokep/django-render-block/pull/32>`_)

0.8.1 (October 15, 2020)
========================

* Fixes a regression in v0.8 where a ``Context`` could not be re-used. Contributed
  by `@evanbrumley <https://github.com/evanbrumley>`_. (`#25 <https://github.com/clokep/django-render-block/pull/25>`_)

0.8 (October 6, 2020)
=====================

* ``render_block_to_string`` now forwards the ``Context`` passed as ``context`` parameter.
  Contributed by `@bblanchon <https://github.com/bblanchon>`_. (`#21 <https://github.com/clokep/django-render-block/pull/21>`_)
* Drop support for Python 3.5, support Python 3.9. (`#22 <https://github.com/clokep/django-render-block/pull/22>`_)

0.7 (July 13, 2020)
===================

* Drop support for Django < 2.2. (`#18 <https://github.com/clokep/django-render-block/pull/18>`_)
* Support Django 3.0 and 3.1. (`#18 <https://github.com/clokep/django-render-block/pull/18>`_,
  `#20 <https://github.com/clokep/django-render-block/pull/20>`_)
* Drop support for Python 2.7. (`#19 <https://github.com/clokep/django-render-block/pull/19>`_)
* Support Python 3.8. (`#18 <https://github.com/clokep/django-render-block/pull/18>`_)

0.6 (May 8, 2019)
=================

* Support Django 1.11, 2.1, and 2.2. (`#9 <https://github.com/clokep/django-render-block/pull/9>`_,
  `#11 <https://github.com/clokep/django-render-block/pull/11>`_,
  `#17 <https://github.com/clokep/django-render-block/pull/17>`_)
* Support Python 2.7, 3.5, 3.6, and 3.7. (`#9 <https://github.com/clokep/django-render-block/pull/9>`_,
  `#17 <https://github.com/clokep/django-render-block/pull/17>`_)
* ``render_block_to_string`` now optionally accepts a ``request`` parameter.
  If given, a ``RequestContext`` instead of a ``Context`` is used when
  rendering with the Django templating engine. Contributed by
  `@vintage <https://github.com/vintage>`_. (`#15 <https://github.com/clokep/django-render-block/pull/15>`_)
* Fix rendering of README on PyPI. Contributed by `@mixxorz <https://github.com/mixxorz>`_.
  (`#10 <https://github.com/clokep/django-render-block/pull/10>`_)

0.5 (September 1, 2016)
=======================

* Fixes a major issue with inheriting templates and rendering a block found in
  the parent template, but overwriting part of it in the child template.
  (`#8 <https://github.com/clokep/django-render-block/pull/8>`_)

0.4 (August 4, 2016)
====================

* Initial support for using the `Jinja2 <http://jinja.pocoo.org/>`_ templating
  engine. See README for caveats. (`#3 <https://github.com/clokep/django-render-block/pull/3>`_)
* Support Django 1.10. (`#5 <https://github.com/clokep/django-render-block/pull/5>`_)
* Support Python 3. (`#6 <https://github.com/clokep/django-render-block/pull/6>`_)

0.3.1 (June 1, 2016)
====================

* Refactoring to make more generic (for potentially supporting multiple
  templating engines).

0.3 (May 27, 2016)
==================

* Largely rewritten.
* Support Django 1.8 and 1.9:

  * Guards against different template backends.
  * Uses internal APIs for each node.
  * Removed ``context_instance`` parameter.
  * Support for calling ``{{ block.super }}``.

0.2.2 (January 10, 2011)
========================

* Updated per
  `comment 3466 on Django Snippet 942 <https://djangosnippets.org/snippets/942/#c3466>`_
  by `eugenyboger <https://djangosnippets.org/users/eugenyboger/>`_
  to fix an issue with nested extends. The specific bug was not reproducible,
  but the additional code shouldn't hurt.

0.2.1 (August 27, 2010)
=======================

* Updated per
  `comment 3237 on Django Snippet 942 <https://djangosnippets.org/snippets/942/#c3237>`_
  by `chadselph <https://djangosnippets.org/users/chadselph/>`_
  to remove a pointless render. The specific bug was not reproducible, but the
  removed code was extraneous.

0.2 (August 4, 2008)
====================

* Updated version from
  `Django Snippet 942 <https://djangosnippets.org/snippets/942/>`_ by
  `zbyte64 <https://djangosnippets.org/users/zbyte64/>`_.
* Improves include:

  1. Simpler/better handling of "extends" block tag
  2. Searches If/Else blocks
  3. Less code
  4. Allow list of templates to be passed which is closer to the behavior of
     ``render_to_response``

0.1 (May 22, 2008)
==================

* Initial version from
  `Django Snippet 769 <https://djangosnippets.org/snippets/769/>`_ by
  `sciyoshi <https://djangosnippets.org/users/sciyoshi/>`_.
* Support Django 0.96.
