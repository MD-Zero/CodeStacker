#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for file_handler.py module.
"""

####################################################################################################

import unittest

class TestFileHandler(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        current_dir = os.path.dirname(__file__)

        self.blueprint_good = os.path.join(current_dir, 'resources/blueprint_good.yaml')
        self.blueprint_nonexistent = os.path.join(current_dir, 'resources/#dummy123.yaml')
        self.blueprint_bad = os.path.join(current_dir, 'resources/blueprint_bad.yaml')
        self.blueprint_empty = os.path.join(current_dir, 'resources/blueprint_empty.yaml')

    def test_all_cases(self):
        """Test all blueprints."""
        from codestacker.exceptions   import TechnicalError
        from codestacker.file_handler import load_yaml

        load_yaml(self.blueprint_good)

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_nonexistent)

        self.assertEqual(context.exception.message, 'file reading error')

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_bad)

        self.assertEqual(context.exception.message, 'YAML parsing error')

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_empty)

        self.assertEqual(context.exception.message, 'empty YAML file')

####################################################################################################

if __name__ == '__main__':
    unittest.main()
