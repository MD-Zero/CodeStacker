#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program flow:
    1. Parse the arguments.
    2. Load the YAML blueprint file content, and choose a configuration.
    3. Validate its inner structure.
    4. TODO
"""

####################################################################################################

def main(arguments):
    """
    Script's main function.
    """
    import os

    from .builder          import build
    from .cleaner          import clean
    from .config_inspector import select_config, validate_config
    from .file_loader      import load_yaml

    command = arguments['command']
    filename = arguments['file']

    config = select_config(load_yaml(filename), arguments['config'])

    root = os.path.dirname(filename)

    validate_config(root, config)

    if command == 'build':
        build(root, config)
    elif command == 'clean':
        clean(root, config)
