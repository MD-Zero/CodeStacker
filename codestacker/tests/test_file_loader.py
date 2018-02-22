#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for file_loader.py module.
"""

####################################################################################################

import unittest

class TestFileLoader(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        current_dir = os.path.dirname(__file__)

        self.blueprint_good = os.path.join(current_dir, 'blueprints/blueprint_good.yaml')
        self.blueprint_nonexistent = os.path.join(current_dir, 'blueprints/#dummy123.yaml')
        self.blueprint_bad = os.path.join(current_dir, 'blueprints/blueprint_bad.yaml')
        self.blueprint_empty = os.path.join(current_dir, 'blueprints/blueprint_empty.yaml')

    def test_blueprints(self):
        """Test all blueprint."""
        from codestacker.exceptions  import TechnicalError
        from codestacker.file_loader import load_yaml

        load_yaml(self.blueprint_good)

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_nonexistent)

        self.assertEqual(context.exception.message, 'file handling error')

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_bad)

        self.assertEqual(context.exception.message, 'YAML parsing error')

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_empty)

        self.assertEqual(context.exception.message, 'empty YAML file')

####################################################################################################

if __name__ == '__main__':
    unittest.main()
