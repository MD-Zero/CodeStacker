#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit test for validator.py module.
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
        from codestacker.config_inspector.validator import validate_config
        from codestacker.errors                     import errors
        from codestacker.errors.exceptions          import FunctionalError

        # Good configuration.
        validate_config(self.config_good)

        # Bad configuration: missing key.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_missing_key)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.MISSING_KEY)

        # Bad configuration: wrong key type.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_wrong_key_type)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.WRONG_KEY_TYPE)

        # Bad configuration: undefined variable.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_undef_var)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.UNDEFINED_VAR)

        # Bad configuration: wrong variable type.
        with self.assertRaises(FunctionalError) as context:
            validate_config(self.config_wrong_var_type)

        context.exception.print()
        self.assertEqual(context.exception.args[0], errors.WRONG_VAR_TYPE)

####################################################################################################

if __name__ == '__main__':
    unittest.main()
