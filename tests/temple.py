import unittest
import os
import os.path as path

import tmplr.temple as temple


class TestTemple(unittest.TestCase):

    def setUp(self):
        self.temples = path.join('tests', 'temples')
        self.example = path.join(self.temples, 'example')

    def test_from_file(self):
        t = temple.from_file(self.example)
        self.assertSequenceEqual(t.placeholders(), ['var', 'func_name'])
        self.assertEqual(t.name, 'example')
        self.assertEqual(t.output, '/tmp/tmplr-test-example-{fname}')
        self.assertEqual(t.help, 'tmux config script')
        self.assertEqual(t.delim, '%%')
        self.assertEqual(
                t.content,
                '''#! /bin/sh
content...
%%var
%%{func_name}
%%var
...etc.
''')

    def test_render(self):
        t = temple.from_file(self.example)
        self.assertEqual(
                t.render(var='my_var', func_name='my_func'),
                '''#! /bin/sh
content...
my_var
my_func
my_var
...etc.
''')

    def test_write(self):
        t = temple.from_file(self.example)
        t.render(var='my_var', func_name='my_func')
        t.write('templar')
        f = t.output.format(fname='templar')
        e = os.path.exists(f)
        if e:
            os.remove(f)
        self.assertTrue(e)

    def test_temples(self):
        temples = temple.temples(self.temples)
        self.assertTrue(temples.keys() == {'example'})
        self.assertTrue(all(
                isinstance(temp, temple.Temple)
                for temp in temples.values()))
