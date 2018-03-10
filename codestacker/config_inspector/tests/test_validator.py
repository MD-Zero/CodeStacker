#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for validitor.py module.
"""

####################################################################################################

import unittest

class TestValidator(unittest.TestCase):
    """
    Test class.
    """
    def setUp(self):
        """Set up."""
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
        from codestacker.errors                     import errors as E
        from codestacker.errors.exceptions          import FunctionalError
        from codestacker.config_inspector.validator import validate_config

        # Good configuration.
        validate_config(self.config_good)

        # Missing key.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_missing_key)

        self.assertEqual(context.exception.args[0], E.MISSING_KEY)
        # self.assertEqual(error[E.MES], E.MISSING_KEY[E.MES])

        # Wrong key type.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_wrong_key_type)

        self.assertEqual(context.exception.args[0], E.WRONG_KEY_TYPE)
        # self.assertEqual(context.exception.args[0], E.WRONG_KEY_TYPE)

        # Undefined variable.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_undef_var)

        self.assertEqual(context.exception.args[0], E.UNDEFINED_VAR)
        # self.assertEqual(context.exception.args[0], E.UNDEFINED_VAR)

        # Wrong variable type.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_wrong_var_type)

        self.assertEqual(context.exception.args[0], E.WRONG_VAR_TYPE)
        # self.assertEqual(message, E.WRONG_VAR_TYPE)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
