#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Errors list.
"""

# File handling errors.
EMPTY_YAML = 'empty YAML file'
FILE_READING = 'file reading error'
YAML_PARSING = 'YAML parsing error'

FILE_WRITING = 'file writing error'
YAML_DUMPING = 'YAML dumping error'

# Configuration inspection errors.
CONFIG_NOT_FOUND = 'configuration "{}" not found'

INCORRECT_KEY_TYPE = 'key "{}" is of incorrect type (should be "{}")'
MISSING_KEY = 'missing mandatory "{}" key'

ERROR_VAR_GRAPH = 'error in variables references ({})'
UNDEFINED_VAR = '"${}" is undefined'
WRONG_VAR_TYPE = '"${}" is not of type "str"'

FOLDER_NOT_FOUND = 'folder "{}" is nonexistent'

# Graph errors.
CYCLES_IN_GRAPH = 'cycle(s) in graph detected'
DEPTH_THRESHOLD = 'depth threshold exceeded'

# Sources inspection errors.
INVALID_FILENAME = 'file "{}" doesn\'t match filenames requirements'

# Build / link errors.
COMPILATION_FAILED = 'compilation failed'
LINKING_FAILED = 'linking failed'
RECIPE_FAILED = 'recipe creation failed'

# Clean-up errors.
REMOVAL_FAILED = 'impossible to remove "{}"'
