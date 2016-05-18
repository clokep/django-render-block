from unittest import TestCase

from django.template import loader, Context

from render_block import render_block_to_string


class TestCases(TestCase):
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
