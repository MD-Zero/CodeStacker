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

def main():
    """
    Script's main function.
    """
    import os
    import sys

    from .args_parser      import parse_args
    from .config_inspector import select_config, validate_config
    from .file_loader      import load_yaml

    options = parse_args()

    filename = os.path.realpath(options['file'])
    config_name = options['config']

    config = select_config(load_yaml(filename), config_name)

    validate_config(os.path.dirname(filename), config)

    sys.exit(0)
