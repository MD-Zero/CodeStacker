#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for utilities.py module.
"""

####################################################################################################

import unittest

class TestUtilities(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        self.source_dir = os.path.join(os.path.dirname(__file__), 'resources')

    def test_validate_sources(self):
        """Test sources validity."""
        from codestacker.constants        import errors as E
        from codestacker.exceptions       import TechnicalError
        from codestacker.system.utilities import check_files

        with self.assertRaises(TechnicalError) as context:
            check_files(self.source_dir, '.cpp')

        self.assertEqual(context.exception.message, E.INVALID_FILENAME.format('Bad# .cpp'))

####################################################################################################

if __name__ == '__main__':
    unittest.main()
