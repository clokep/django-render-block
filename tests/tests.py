from unittest import TestCase

from django.template import loader, Context

from template import render_block_to_string


class TestCases(TestCase):
    def test_1(self):
        result = render_block_to_string('test2.html', 'block1', Context({}))
        self.assertEqual(result, u'block1 from test2')

    def test_2(self):
        result = render_block_to_string('test2.html', 'block2', Context({}))
        self.assertEqual(result, u'block2 from test1')
