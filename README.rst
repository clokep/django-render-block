Django Render Block
###################

Allows getting the rendered content of a specific block tag. Useful if you want
to send just a part of a template back for an AJAX request. Works for arbitrary
template inheritance, even if a block is defined in the child template but not
in the parent.

Example:

In `test1.html`:

```jinja
{% block block1 %}block1 from test1{% endblock %}
{% block block2 %}block2 from test1{% endblock %}
```

In `test2.html`:

```jinja
{% extends 'test1.html' %}
{% block block1 %}block1 from test2{% endblock %}
```

And from the Python shell:

```python
>>> from django.template import loader, Context
>>> from template import render_block_to_string
>>> print render_block_to_string('test2.html', 'block1', Context({}))
u'block1 from test2'
>>> print render_block_to_string('test2.html', 'block2', Context({}))
u'block2 from test1'
```

Attribution
===========

This is based on a few DjangoSnippets:

* Originally https://djangosnippets.org/snippets/769/
* Updated version https://djangosnippets.org/snippets/942/
* A version of those https://github.com/uniphil/Django-Block-Render/
* Also based on a StackOverflow answer: http://stackoverflow.com/questions/2687173/django-how-can-i-get-a-block-from-a-template
* And https://github.com/BradWhittington/django-templated-email/blob/master/templated_email/utils.py
