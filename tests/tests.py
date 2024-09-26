from unittest import skip
from unittest.mock import patch

from django.template import Context
from django.test import (
    Client,
    RequestFactory,
    TestCase,
    modify_settings,
    override_settings,
)
from django.test.signals import template_rendered
from django.urls import reverse

from render_block import BlockNotFound, UnsupportedEngine, render_block_to_string


class TestRenderBlockToStringForDjango(TestCase):
    """Test render_block_to_string for the Django templating engine."""

    def assertExceptionMessageEquals(self, exception: Exception, expected: str) -> None:
        self.assertEqual(expected, exception.args[0])

    def test_block(self) -> None:
        """Test rendering an individual block."""
        result = render_block_to_string("test1.html", "block1")
        self.assertEqual(result, "block1 from test1")

        # No reason this shouldn't work, but just in case.
        result = render_block_to_string("test1.html", "block2")
        self.assertEqual(result, "block2 from test1")

    def test_override(self) -> None:
        """This block is overridden in test2."""
        result = render_block_to_string("test2.html", "block1")
        self.assertEqual(result, "block1 from test2")

    def test_inherit(self) -> None:
        """This block is inherited from test1."""
        result = render_block_to_string("test2.html", "block2")
        self.assertEqual(result, "block2 from test1")

    def test_inherit_context(self) -> None:
        """This block is inherited from test1."""
        result = render_block_to_string(
            "test2.html", "block2", Context({"suffix2": " blah"})
        )
        self.assertEqual(result, "block2 from test1 blah")

    def test_multi_inherited(self) -> None:
        """A block from an included template should be available."""
        result = render_block_to_string("test4.html", "block2")
        self.assertEqual(result, "block2 from test1")

    def test_multi_inherited_context(self) -> None:
        """A block from an included template should be available."""
        result = render_block_to_string(
            "test4.html", "block2", Context({"suffix2": " blah"})
        )
        self.assertEqual(result, "block2 from test1 blah")

    def test_no_block(self) -> None:
        """Check if there's no block available an exception is raised."""
        with self.assertRaises(BlockNotFound) as exc:
            render_block_to_string("test1.html", "noblock")
        self.assertExceptionMessageEquals(
            exc.exception, "block with name 'noblock' does not exist"
        )

    def test_include(self) -> None:
        """Ensure that an include tag in a block still works."""
        result = render_block_to_string("test3_django.html", "block1")
        self.assertEqual(result, "included template")

    def test_super(self) -> None:
        """Test that block.super works."""
        result = render_block_to_string("test3_django.html", "block2")
        self.assertEqual(result, "block2 from test3 - block2 from test1")

    def test_multi_super(self) -> None:
        result = render_block_to_string("test6_django.html", "block2")
        self.assertEqual(
            result, "block2 from test6 - block2 from test3 - block2 from test1"
        )

    def test_super_with_same_context_on_multiple_executions(self) -> None:
        """Test that block.super works when fed the same context object twice."""
        context = Context()
        result_one = render_block_to_string(
            "test3_django.html", "block2", context=context
        )
        result_two = render_block_to_string(
            "test3_django.html", "block2", context=context
        )
        self.assertEqual(
            result_one, result_two, "block2 from test3 - block2 from test1"
        )

    def test_subblock(self) -> None:
        """Test that a block within a block works."""
        result = render_block_to_string("test5.html", "block1")
        self.assertEqual(result, "block3 from test5")

        result = render_block_to_string("test5.html", "block3")
        self.assertEqual(result, "block3 from test5")

    def test_subblock_no_parent(self) -> None:
        """
        Test that a block within a block works if the parent block is only found
        in the base template.

        This is very similar to test_subblock, but the templates differ. In this
        test the sub-template does not replace the entire block from the parent
        template.
        """
        result = render_block_to_string("test_sub.html", "base")
        self.assertEqual(result, "\n\nbar\n\n")

        result = render_block_to_string("test_sub.html", "first")
        self.assertEqual(result, "\nbar\n")

    def test_exceptions(self) -> None:
        with self.assertRaises(Exception) as e:
            render_block_to_string("test_exception.html", "exception_block")
        self.assertEqual(str(e.exception), "Exception raised in template tag.")

    @override_settings(DEBUG=True)
    def test_exceptions_debug(self) -> None:
        with self.assertRaises(Exception) as exc:
            render_block_to_string("test_exception.html", "exception_block")
        self.assertExceptionMessageEquals(
            exc.exception, "Exception raised in template tag."
        )

    def test_context(self) -> None:
        """Test that a context is properly rendered in a template."""
        data = "block2 from test5"
        result = render_block_to_string("test5.html", "block2", {"foo": data})
        self.assertEqual(result, data)

    def test_context_autoescape_off(self) -> None:
        """Test that the user can disable autoescape by providing a Context instance."""
        data = "&'"
        result = render_block_to_string(
            "test5.html", "block2", Context({"foo": data}, autoescape=False)
        )
        self.assertEqual(result, data)

    @override_settings(
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.dummy.TemplateStrings",
                "DIRS": ["tests/templates"],
                "APP_DIRS": True,
            }
        ]
    )
    def test_different_backend(self) -> None:
        """
        Ensure an exception is thrown if a different backed from the Django
        backend is used.
        """
        with self.assertRaises(UnsupportedEngine) as exc:
            render_block_to_string("test1.html", "noblock")
        self.assertExceptionMessageEquals(
            exc.exception, "Can only render blocks from the Django template backend."
        )

    @modify_settings(
        INSTALLED_APPS={
            "prepend": [
                "django.contrib.auth",
                "django.contrib.contenttypes",
            ],
        },
    )
    def test_request_context(self) -> None:
        """Test that a request context data are properly rendered in a template."""
        request = RequestFactory().get("dummy-url")
        result = render_block_to_string(
            "test_request_context.html", "block1", {}, request
        )

        self.assertEqual(result, "/dummy-url")


@modify_settings(
    INSTALLED_APPS={
        "prepend": [
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
    },
)
class TestRenderBlockForDjango(TestCase):
    """Test render_block for the Django templating engine."""

    def setUp(self):
        self.mock_method = patch(
            "render_block.BlockOfTemplateResponse.notify_block_render"
        ).start()
        self.mock_method.side_effect = lambda template, context: template_rendered.send(
            sender=None, template=template, context=context
        )

    def tearDown(self):
        self.mock_method.stop()

    def assertExceptionMessageEquals(self, exception: Exception, expected: str) -> None:
        self.assertEqual(expected, exception.args[0])

    def test_block(self) -> None:
        client = Client()
        data = {
            "template_name": "test5.html",
            "block_name": "block2",
            "foo": "bar",
        }
        response = client.post(reverse("block"), data=data)

        result = response.content.decode("utf-8")
        self.assertEqual(result, "bar")
        self.assertEquals(response.context["foo"], "bar")

    @override_settings(
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.dummy.TemplateStrings",
                "DIRS": ["tests/templates"],
                "APP_DIRS": True,
            }
        ]
    )
    def test_different_backend(self) -> None:
        """
        Ensure an exception is thrown if a different backed from the Django
        backend is used.
        """
        client = Client()
        data = {
            "template_name": "test5.html",
            "block_name": "block2",
            "foo": "bar",
        }
        with self.assertRaises(UnsupportedEngine) as exc:
            client.post(reverse("block"), data=data)

        self.assertExceptionMessageEquals(
            exc.exception, "Can only render blocks from the Django template backend."
        )


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.jinja2.Jinja2",
            "DIRS": ["tests/templates"],
            "APP_DIRS": True,
        }
    ]
)
class TestRenderBlockToStringForJinja2(TestCase):
    """Test render_block_to_string for the Jinja2 templating engine."""

    def assertExceptionMessageEquals(self, exception: Exception, expected: str) -> None:
        self.assertEqual(expected, exception.args[0])

    def test_block(self) -> None:
        """Test rendering an individual block."""
        result = render_block_to_string("test1.html", "block1")
        self.assertEqual(result, "block1 from test1")

        # No reason this shouldn't work, but just in case.
        result = render_block_to_string("test1.html", "block2")
        self.assertEqual(result, "block2 from test1")

    def test_override(self) -> None:
        """This block is overridden in test2."""
        result = render_block_to_string("test2.html", "block1")
        self.assertEqual(result, "block1 from test2")

    @skip("Not currently supported.")
    def test_inherit(self) -> None:
        """This block is inherited from test1."""
        result = render_block_to_string("test2.html", "block2")
        self.assertEqual(result, "block2 from test1")

    def test_no_block(self) -> None:
        """Check if there's no block available an exception is raised."""
        with self.assertRaises(BlockNotFound) as exc:
            render_block_to_string("test1.html", "noblock")
        self.assertExceptionMessageEquals(
            exc.exception, "block with name 'noblock' does not exist"
        )

    def test_include(self) -> None:
        """Ensure that an include tag in a block still works."""
        result = render_block_to_string("test3_jinja2.html", "block1")
        self.assertEqual(result, "included template")

    @skip("Not currently supported.")
    def test_super(self) -> None:
        """Test that super() works."""
        result = render_block_to_string("test3_jinja2.html", "block2")
        self.assertEqual(result, "block2 from test3 - block2 from test1")

    @skip("Not currently supported.")
    def test_multi_super(self) -> None:
        result = render_block_to_string("test6_jinja2.html", "block2")
        self.assertEqual(
            result, "block2 from test6 - block2 from test3 - block2 from test1"
        )

    @skip("Not currently supported.")
    def test_multi_inherited(self) -> None:
        """A block from an included template should be available."""
        result = render_block_to_string("test4.html", "block2")
        self.assertEqual(result, "block2 from test1")

    def test_subblock(self) -> None:
        """Test that a block within a block works."""
        result = render_block_to_string("test5.html", "block1")
        self.assertEqual(result, "block3 from test5")

        result = render_block_to_string("test5.html", "block3")
        self.assertEqual(result, "block3 from test5")

    @skip("Not currently supported.")
    def test_subblock_no_parent(self) -> None:
        """
        Test that a block within a block works if the parent block is only found
        in the base template.

        This is very similar to test_subblock, but the templates differ. In this
        test the sub-template does not replace the entire block from the parent
        template.
        """
        result = render_block_to_string("test_sub.html", "base")
        self.assertEqual(result, "\n\nbar\n\n")

        result = render_block_to_string("test_sub.html", "first")
        self.assertEqual(result, "\nbar\n")

    def test_context(self) -> None:
        """Test that a context is properly rendered in a template."""
        data = "block2 from test5"
        result = render_block_to_string("test5.html", "block2", {"foo": data})
        self.assertEqual(result, data)


@override_settings(
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.jinja2.Jinja2",
            "DIRS": ["tests/templates"],
            "APP_DIRS": True,
        }
    ]
)
class TestRenderBlockForJinja2(TestCase):
    """Test render_block for the Jinja2 templating engine."""

    def setUp(self):
        self.mock_method = patch(
            "render_block.BlockOfTemplateResponse.notify_block_render"
        ).start()
        self.mock_method.side_effect = lambda template, context: template_rendered.send(
            sender=None, template=template, context=context
        )

    def tearDown(self):
        self.mock_method.stop()

    def assertExceptionMessageEquals(self, exception: Exception, expected: str) -> None:
        self.assertEqual(expected, exception.args[0])

    def test_block(self) -> None:
        client = Client()
        data = {
            "template_name": "test5.html",
            "block_name": "block2",
            "foo": "bar",
        }
        response = client.post(reverse("block"), data=data)

        result = response.content.decode("utf-8")
        self.assertEqual(result, "bar")
        self.assertEquals(response.context["foo"], "bar")

    @override_settings(
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.dummy.TemplateStrings",
                "DIRS": ["tests/templates"],
                "APP_DIRS": True,
            }
        ]
    )
    def test_different_backend(self) -> None:
        """
        Ensure an exception is thrown if a different backed from the Django
        backend is used.
        """
        client = Client()
        data = {
            "template_name": "test5.html",
            "block_name": "block2",
            "foo": "bar",
        }
        with self.assertRaises(UnsupportedEngine) as exc:
            client.post(reverse("block"), data=data)

        self.assertExceptionMessageEquals(
            exc.exception, "Can only render blocks from the Django template backend."
        )
