Django Render Block
###################

Render the content of a specific block tag from a Django template. Works for
arbitrary template inheritance, even if a block is defined in the child template
but not in the parent. Generally it works like ``render_to_string`` from Django,
but allows you to specify a block to render.

Example:

In ``test1.html``:

.. code-block:: jinja

    {% block block1 %}block1 from test1{% endblock %}
    {% block block2 %}block2 from test1{% endblock %}

In ``test2.html``:

.. code-block:: jinja

    {% extends 'test1.html' %}
    {% block block1 %}block1 from test2{% endblock %}

And from the Python shell:

.. code-block:: python

    >>> from render_block import render_block_to_string
    >>> print render_block_to_string('test2.html', 'block1')
    u'block1 from test2'
    >>> print render_block_to_string('test2.html', 'block2')
    u'block2 from test1'

It can also accept a context as a ``dict`` (just like ``render_to_string``), in
``test3.html``:

.. code-block:: jinja

    {% block block3 %}Render this {{ variable }}!{% endblock %}

And from Python:

.. code-block:: python

    >>> print render_block_to_string('test3.html', 'block3', {'variable': 'test'})
    u'Render this test!'

Requirements
============

This has been tested on Django 1.8 and 1.9. You must use the Django template
rendering engine (the default) for any templates which you wish to render a
block from.

Attribution
===========

This is based on a few sources:

* Originally `Django Snippet 769 <https://djangosnippets.org/snippets/769/>`_
* Updated version `Django Snippet 942 <https://djangosnippets.org/snippets/942/>`_
* A version of the snippets was ported as `Django-Block-Render <https://github.com/uniphil/Django-Block-Render/>`_
* Additionally inspired by part of `django-templated-email <https://github.com/BradWhittington/django-templated-email/blob/master/templated_email/utils.py>`_
* Also based on a `StackOverflow answer 2687173 <http://stackoverflow.com/questions/2687173/django-how-can-i-get-a-block-from-a-template>`_
