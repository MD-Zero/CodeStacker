#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for file_loader.py module.
"""

####################################################################################################

import unittest

class TestFileLoader(unittest.TestCase):
    """
    Test class for file_loader.py module's content.
    """
    def setUp(self):
        """Set up."""
        import os

        self.blueprint_good = os.path.join(os.path.dirname(__file__), 'blueprint_good.yaml')
        self.blueprint_nonexistent = os.path.join(os.path.dirname(__file__), '#dummy123')
        self.blueprint_bad = os.path.join(os.path.dirname(__file__), 'blueprint_bad.yaml')
        self.blueprint_empty = os.path.join(os.path.dirname(__file__), 'blueprint_empty.yaml')

    def test_blueprint_good(self):
        """Test good blueprint."""
        from codestacker.file_loader import load_yaml

        load_yaml(self.blueprint_good)

    def test_blueprint_nonexistent(self):
        """Test no blueprint."""
        from codestacker.exceptions  import TechnicalError
        from codestacker.file_loader import load_yaml

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_nonexistent)

        self.assertEqual(context.exception.get_message(), 'file handling error')

    def test_blueprint_bad(self):
        """Test bad blueprint."""
        from codestacker.exceptions  import TechnicalError
        from codestacker.file_loader import load_yaml

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_bad)

        self.assertEqual(context.exception.get_message(), 'YAML parsing error')

    def test_blueprint_empty(self):
        """Test empty blueprint."""
        from codestacker.exceptions  import TechnicalError
        from codestacker.file_loader import load_yaml

        with self.assertRaises(TechnicalError) as context:
            load_yaml(self.blueprint_empty)

        self.assertEqual(context.exception.get_message(), 'empty YAML file')

####################################################################################################

if __name__ == '__main__':
    unittest.main()
