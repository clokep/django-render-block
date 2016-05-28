from unittest import skip, TestCase

from django.template import Context
from django.utils import six

from render_block import render_block_to_string, BlockNotFound


class TestCases(TestCase):
    def assertExceptionMessageEquals(self, exception, expected):
        result = exception.message if six.PY2 else exception.args[0]
        self.assertEqual(expected, result)

    def test_block(self):
        """Test rendering an individual block."""
        result = render_block_to_string('test1.html', 'block1', Context({}))
        self.assertEqual(result, u'block1 from test1')

        # No reason this shouldn't work, but just in case.
        result = render_block_to_string('test1.html', 'block2', Context({}))
        self.assertEqual(result, u'block2 from test1')

    def test_override(self):
        """This block is overridden in test2."""
        result = render_block_to_string('test2.html', 'block1', Context({}))
        self.assertEqual(result, u'block1 from test2')

    def test_inherit(self):
        """This block is inherited from test1."""
        result = render_block_to_string('test2.html', 'block2', Context({}))
        self.assertEqual(result, u'block2 from test1')

    def test_no_block(self):
        """Check if there's no block available an exception is raised."""
        with self.assertRaises(BlockNotFound) as exc:
            render_block_to_string('test1.html', 'noblock')
        self.assertExceptionMessageEquals(exc.exception,
                                          "block with name 'noblock' does not exist")

    def test_include(self):
        """Ensure that an include tag in a block still works."""
        result = render_block_to_string('test3.html', 'block1', Context({}))
        self.assertEqual(result, u'included template')

    def test_super(self):
        """Test that block.super works."""
        result = render_block_to_string('test3.html', 'block2', Context({}))
        self.assertEqual(result, u'block2 from test3 - block2 from test1')

    def test_subblock(self):
        """Test that a block within a block works."""
        result = render_block_to_string('test5.html', 'block1', Context({}))
        self.assertEqual(result, u'block3 from test5')

        result = render_block_to_string('test5.html', 'block3', Context({}))
        self.assertEqual(result, u'block3 from test5')
