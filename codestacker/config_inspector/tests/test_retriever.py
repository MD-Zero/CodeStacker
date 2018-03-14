#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for retriever.py module.
"""

####################################################################################################

import unittest

class TestRetriever(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        self.arguments_good = {
            'file': os.path.join(os.path.dirname(__file__), 'resources/blueprint.yaml'),
            'command': 'build',
            'config': 'default'}

        self.arguments_bad = {
            'file': os.path.join(os.path.dirname(__file__), 'resources/blueprint.yaml'),
            'command': 'clean',
            'config': '#dummy#'}

    def test_get_config(self):
        """Test configuration retrieval mechanism."""
        from codestacker.config_inspector.retriever import get_config
        from codestacker.errors                     import errors
        from codestacker.errors.exceptions          import TechnicalError

        # Good arguments.
        get_config(self.arguments_good)

        # Bad arguments: unknown configuration name.
        with self.assertRaises(TechnicalError) as context:
            get_config(self.arguments_bad)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.CONFIG_NOT_FOUND)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
