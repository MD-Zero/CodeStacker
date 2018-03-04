#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for config_inspector.py module.
"""

####################################################################################################

import unittest

class TestConfigInspector(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
        import os

        self.config_good = {
            'binary': 'bin',
            'build': 'build',
            'flags': ['-Wall', '-Werror', '-g', '-pedantic-errors'],
            'include': 'src',
            'libraries': ['glfw'],
            'output': 'Test',
            'sources': '$include'}

        self.config_missing_key = {
            'binary': 'bin',
            'build': 'build',
            'flags': ['-Wall', '-Werror', '-g', '-pedantic-errors'],
            'include': 'src',
            'libraries': ['glfw'],
            'sources': '$include'}

        self.config_wrong_key_type = {
            'binary': 'bin',
            'build': 'build',
            'flags': 42,
            'include': 'src',
            'libraries': ['glfw'],
            'output': 'Test',
            'sources': '$include'}

        self.config_undef_var = {
            'binary': 'bin',
            'build': 'build',
            'flags': ['-Wall', '-Werror', '-g', '-pedantic-errors'],
            'include': 'src',
            'libraries': ['glfw'],
            'output': 'Test',
            'sources': '$target'}

        self.config_wrong_var_type = {
            'binary': 'bin',
            'build': 'build',
            'flags': ['-Wall', '-Werror', '-g', '-pedantic-errors'],
            'include': 'src',
            'libraries': ['glfw'],
            'output': 'Test',
            'sources': '$flags'}

    def test_validate_sources(self):
        """Test configuration validity."""
        from codestacker                  import errors as E
        from codestacker.exceptions       import FunctionalError, TechnicalError
        from codestacker.config_inspector import validate_config

        validate_config(self.config_good)

        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_missing_key)

        self.assertEqual(context.exception.message, E.MISSING_KEY.format('output'))

        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_wrong_key_type)

        self.assertEqual(context.exception.message, E.INCORRECT_KEY_TYPE.format('flags', 'list'))

        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_undef_var)

        self.assertEqual(context.exception.message, E.UNDEFINED_VAR.format('target'))

        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_wrong_var_type)

        self.assertEqual(context.exception.message, E.WRONG_VAR_TYPE.format('flags'))

####################################################################################################

if __name__ == '__main__':
    unittest.main()
