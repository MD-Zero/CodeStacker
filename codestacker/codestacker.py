#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program flow:
    1. Parse the arguments.
    2. Load the YAML configuration file content.
    3. Validate its inner structure.
    4. TODO
"""

####################################################################################################

def main():
    """
    Script's main function.
    """
    import sys

    from .args_parser      import parse_args
    from .file_loader      import load_yaml
    from .config_inspector import select_config, validate_config

    options = parse_args()

    config = select_config(load_yaml(options['file']), options['config'])

    validate_config(config)

    sys.exit(0)
