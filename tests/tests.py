from unittest import TestCase

from django.template import Context
from django.utils import six

from render_block import render_block_to_string, BlockNotFound


class TestCases(TestCase):
    def assertExceptionMessageEquals(self, exception, expected):
        result = exception.message if six.PY2 else exception.args[0]
        self.assertEqual(expected, result)

    def test_html1_block1(self):
        result = render_block_to_string('test1.html', 'block1', Context({}))
        self.assertEqual(result, u'block1 from test1')

    def test_html1_block2(self):
        result = render_block_to_string('test1.html', 'block2', Context({}))
        self.assertEqual(result, u'block2 from test1')

    def test_html2_block1(self):
        """This block is overridden in html1."""
        result = render_block_to_string('test2.html', 'block1', Context({}))
        self.assertEqual(result, u'block1 from test2')

    def test_html2_block2(self):
        """This block is inherited from html1."""
        result = render_block_to_string('test2.html', 'block2', Context({}))
        self.assertEqual(result, u'block2 from test1')

    def test_no_block(self):
        """Check if there's no block available an exception is raised."""
        with self.assertRaises(BlockNotFound) as exc:
            render_block_to_string('test1.html', 'noblock')
        self.assertExceptionMessageEquals(exc.exception,
                                          "block with name 'noblock' does not exist")
