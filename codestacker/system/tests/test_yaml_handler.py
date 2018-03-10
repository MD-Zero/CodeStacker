#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for yaml_handler.py module.
"""

####################################################################################################

import unittest

class TestYamlHandler(unittest.TestCase):
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
        from codestacker.errors              import errors as E
        from codestacker.errors.exceptions   import FileSystemError, TechnicalError
        from codestacker.system.yaml_handler import load_yaml

        # Good blueprint.
        load_yaml(self.blueprint_good)

        # Non-existent blueprint.
        with self.assertRaises(FileSystemError) as context:
            load_yaml(self.blueprint_nonexistent)

        self.assertEqual(context.exception.args[0], E.FILE_READING)

        # Bad blueprint.
        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_bad)

        self.assertEqual(context.exception.args[0], E.YAML_PARSING)

        # Empty blueprint.
        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_empty)

        self.assertEqual(context.exception.args[0], E.EMPTY_YAML)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
