#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program flow:
    1. Parse the arguments.
    2. TODO
"""

def main():
    """
    Script's main function.
    """
    import sys

    from .args_parser import parse_args
    from .file_loader import load_yaml

    options = parse_args()
    content = load_yaml(options['file'])

    sys.exit()
