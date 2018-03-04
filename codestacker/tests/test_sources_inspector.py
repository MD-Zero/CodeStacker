#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for sources_inspector.py module.
"""

####################################################################################################

import unittest

class TestSourcesInspector(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        self.source_dir = os.path.join(os.path.dirname(__file__), 'resources')

        self.source_good = 'Good.hpp'
        self.source_bad = 'Bad# .cpp'

    def test_validate_sources(self):
        """Test sources validity."""
        from codestacker                   import errors as E
        from codestacker.exceptions        import TechnicalError
        from codestacker.sources_inspector import validate_sources

        with self.assertRaises(TechnicalError) as context:
            validate_sources(self.source_dir, self.source_dir)

        self.assertEqual(context.exception.message, E.INVALID_FILENAME.format(self.source_bad))

####################################################################################################

if __name__ == '__main__':
    unittest.main()
