#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for adaptor.py module.
"""

####################################################################################################

import unittest

class TestAdaptor(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        self.bin_dir = os.path.join(os.path.dirname(__file__), 'resources', 'bin')
        self.build_dir = os.path.join(os.path.dirname(__file__), 'resources', 'build')
        self.src_dir = os.path.join(os.path.dirname(__file__), 'resources', 'src')

        os.makedirs(self.src_dir)

        self.config_good = {
            '_command': 'build',
            '_root': os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources')),
            'binary': 'bin',
            'build': 'build',
            'include': 'src',
            'output': 'Test',
            'sources': 'src'}

        self.config_bad = {
            '_command': 'clean',
            '_root': os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources')),
            'binary': 'bin',
            'build': 'build',
            'include': 'src',
            'output': 'Test',
            'sources': 'dummy'}

    def tearDown(self):
        """Tear down."""
        import os

        if os.path.isdir(self.bin_dir):
            os.rmdir(self.bin_dir)
        if os.path.isdir(self.build_dir):
            os.rmdir(self.build_dir)
        if os.path.isdir(self.src_dir):
            os.rmdir(self.src_dir)

    def test_adapt_config(self):
        """Test configuration adaptation."""
        import os

        from codestacker.config_inspector.adaptor import adapt_config
        from codestacker.constants                import keys
        from codestacker.errors                   import errors
        from codestacker.errors.exceptions        import TechnicalError

        # Valid configuration.
        adapt_config(self.config_good)

        self.assertTrue(os.path.isdir(self.bin_dir))
        self.assertTrue(os.path.isdir(self.build_dir))

        self.assertTrue(isinstance(self.config_good[keys.FLAGS], set))
        self.assertTrue(isinstance(self.config_good[keys.LIBRARIES], set))

        # Non-existent mandatory directory.
        with self.assertRaises(TechnicalError) as context:
            adapt_config(self.config_bad)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.FOLDER_NOT_FOUND)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
