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

        self.blueprint_good = os.path.join(current_dir, 'resources', 'blueprint_good.yaml')
        self.blueprint_nonexistent = os.path.join(current_dir, 'resources', '#dummy#.yaml')
        self.blueprint_broken = os.path.join(current_dir, 'resources', 'blueprint_broken.yaml')
        self.blueprint_empty = os.path.join(current_dir, 'resources', 'blueprint_empty.yaml')

    def test_all_cases(self):
        """Test all blueprints."""
        from codestacker.errors              import errors
        from codestacker.errors.exceptions   import FileSystemError, TechnicalError
        from codestacker.system.yaml_handler import load_yaml

        # Good blueprint.
        load_yaml(self.blueprint_good)

        # Bad blueprint: non-existent.
        with self.assertRaises(FileSystemError) as context:
            load_yaml(self.blueprint_nonexistent)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.FILE_READING_ERROR)

        # Bad blueprint: ill-formed YAML.
        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_broken)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.YAML_PARSING_ERROR)

        # Bad blueprint: empty file.
        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_empty)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.EMPTY_YAML)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
