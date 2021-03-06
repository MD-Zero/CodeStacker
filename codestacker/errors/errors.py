#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Errors list.
"""

# File handling errors.
FILE_READING_ERROR = 'file reading error'
YAML_PARSING_ERROR = 'YAML parsing error'

EMPTY_YAML = 'empty YAML file'

FILE_WRITING_ERROR = 'file writing error'
YAML_DUMPING_ERROR = 'YAML dumping error'

# Configuration inspection errors.
CONFIG_NOT_FOUND = 'configuration not found'

MISSING_KEY = 'missing mandatory key'
WRONG_KEY_TYPE = 'key is of incorrect type'

VAR_GRAPH_ERROR = 'error in variables references'
UNDEFINED_VAR = 'variable is undefined'
WRONG_VAR_TYPE = 'variable is not of type "str"'

FOLDER_NOT_FOUND = 'folder is nonexistent'

# Graph errors.
CYCLES_IN_GRAPH = 'cycle(s) in graph detected'
GRAPH_TOO_DEEP = 'depth threshold exceeded'

# Sources inspection errors.
INVALID_FILENAME = 'file doesn\'t match filenames requirements'

# Build / link errors.
INVALID_OUTPUT_NAME = 'invalid output name'

COMPILATION_FAILED = 'compilation failed'
LINKING_FAILED = 'linking failed'
RECIPE_FAILED = 'recipe creation failed'

# Clean-up errors.
REMOVAL_FAILED = 'removal failed'
