from unittest import skip

from django.test import modify_settings, override_settings, TestCase, RequestFactory
try:
    from django.utils import six
    PY2 = six.PY2
except ImportError:
    # Django > 3 does not include six.
    PY2 = False

from render_block import render_block_to_string, BlockNotFound, UnsupportedEngine


class TestDjango(TestCase):
    """Test the Django templating engine."""
    def assertExceptionMessageEquals(self, exception, expected):
        result = exception.message if PY2 else exception.args[0]
        self.assertEqual(expected, result)

    def test_block(self):
        """Test rendering an individual block."""
        result = render_block_to_string('test1.html', 'block1')
        self.assertEqual(result, 'block1 from test1')

        # No reason this shouldn't work, but just in case.
        result = render_block_to_string('test1.html', 'block2')
        self.assertEqual(result, 'block2 from test1')

    def test_override(self):
        """This block is overridden in test2."""
        result = render_block_to_string('test2.html', 'block1')
        self.assertEqual(result, 'block1 from test2')

    def test_inherit(self):
        """This block is inherited from test1."""
        result = render_block_to_string('test2.html', 'block2')
        self.assertEqual(result, 'block2 from test1')

    def test_no_block(self):
        """Check if there's no block available an exception is raised."""
        with self.assertRaises(BlockNotFound) as exc:
            render_block_to_string('test1.html', 'noblock')
        self.assertExceptionMessageEquals(exc.exception,
                                          "block with name 'noblock' does not exist")

    def test_include(self):
        """Ensure that an include tag in a block still works."""
        result = render_block_to_string('test3_django.html', 'block1')
        self.assertEqual(result, 'included template')

    def test_super(self):
        """Test that block.super works."""
        result = render_block_to_string('test3_django.html', 'block2')
        self.assertEqual(result, 'block2 from test3 - block2 from test1')

    def test_multi_super(self):
        result = render_block_to_string('test6_django.html', 'block2')
        self.assertEqual(result, 'block2 from test6 - block2 from test3 - block2 from test1')

    def test_subblock(self):
        """Test that a block within a block works."""
        result = render_block_to_string('test5.html', 'block1')
        self.assertEqual(result, 'block3 from test5')

        result = render_block_to_string('test5.html', 'block3')
        self.assertEqual(result, 'block3 from test5')

    def test_subblock_no_parent(self):
        """
        Test that a block within a block works if the parent block is only found
        in the base template.

        This is very similar to test_subblock, but the templates differ. In this
        test the sub-template does not replace the entire block from the parent
        template.
        """
        result = render_block_to_string('test_sub.html', 'base')
        self.assertEqual(result, '\n\nbar\n\n')

        result = render_block_to_string('test_sub.html', 'first')
        self.assertEqual(result, '\nbar\n')

    def test_context(self):
        """Test that a context is properly rendered in a template."""
        data = 'block2 from test5'
        result = render_block_to_string('test5.html', 'block2', {'foo': data})
        self.assertEqual(result, data)

    @override_settings(
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.dummy.TemplateStrings',
            'DIRS': ['tests/templates'],
            'APP_DIRS': True,
        }]
    )
    def test_different_backend(self):
        """
        Ensure an exception is thrown if a different backed from the Django
        backend is used.
        """
        with self.assertRaises(UnsupportedEngine) as exc:
            render_block_to_string('test1.html', 'noblock')
        self.assertExceptionMessageEquals(exc.exception,
                                          "Can only render blocks from the Django template backend.")

    @modify_settings(
        INSTALLED_APPS={
            'prepend': [
                'django.contrib.auth',
                'django.contrib.contenttypes',
            ],
        },
    )
    def test_request_context(self):
        """Test that a request context data are properly rendered in a template."""
        request = RequestFactory().get('dummy-url')
        result = render_block_to_string('test_request_context.html', 'block1', {}, request)

        self.assertEqual(result, '/dummy-url')


@override_settings(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': ['tests/templates'],
        'APP_DIRS': True,
    }]
)
class TestJinja2(TestCase):
    """Test the Django templating engine."""
    def assertExceptionMessageEquals(self, exception, expected):
        result = exception.message if PY2 else exception.args[0]
        self.assertEqual(expected, result)

    def test_block(self):
        """Test rendering an individual block."""
        result = render_block_to_string('test1.html', 'block1')
        self.assertEqual(result, 'block1 from test1')

        # No reason this shouldn't work, but just in case.
        result = render_block_to_string('test1.html', 'block2')
        self.assertEqual(result, 'block2 from test1')

    def test_override(self):
        """This block is overridden in test2."""
        result = render_block_to_string('test2.html', 'block1')
        self.assertEqual(result, 'block1 from test2')

    @skip('Not currently supported.')
    def test_inherit(self):
        """This block is inherited from test1."""
        result = render_block_to_string('test2.html', 'block2')
        self.assertEqual(result, 'block2 from test1')

    def test_no_block(self):
        """Check if there's no block available an exception is raised."""
        with self.assertRaises(BlockNotFound) as exc:
            render_block_to_string('test1.html', 'noblock')
        self.assertExceptionMessageEquals(exc.exception,
                                          "block with name 'noblock' does not exist")

    def test_include(self):
        """Ensure that an include tag in a block still works."""
        result = render_block_to_string('test3_jinja2.html', 'block1')
        self.assertEqual(result, 'included template')

    @skip('Not currently supported.')
    def test_super(self):
        """Test that super() works."""
        result = render_block_to_string('test3_jinja2.html', 'block2')
        self.assertEqual(result, 'block2 from test3 - block2 from test1')

    @skip('Not currently supported.')
    def test_multi_super(self):
        result = render_block_to_string('test6_jinja2.html', 'block2')
        self.assertEqual(result, 'block2 from test6 - block2 from test3 - block2 from test1')

    def test_subblock(self):
        """Test that a block within a block works."""
        result = render_block_to_string('test5.html', 'block1')
        self.assertEqual(result, 'block3 from test5')

        result = render_block_to_string('test5.html', 'block3')
        self.assertEqual(result, 'block3 from test5')

    @skip('Not currently supported.')
    def test_subblock_no_parent(self):
        """
        Test that a block within a block works if the parent block is only found
        in the base template.

        This is very similar to test_subblock, but the templates differ. In this
        test the sub-template does not replace the entire block from the parent
        template.
        """
        result = render_block_to_string('test_sub.html', 'base')
        self.assertEqual(result, '\n\nbar\n\n')

        result = render_block_to_string('test_sub.html', 'first')
        self.assertEqual(result, '\nbar\n')

    def test_context(self):
        """Test that a context is properly rendered in a template."""
        data = 'block2 from test5'
        result = render_block_to_string('test5.html', 'block2', {'foo': data})
        self.assertEqual(result, data)
