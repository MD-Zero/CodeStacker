#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Argument parsing utility.
"""

####################################################################################################

_FILE_DESC = '''specify the blueprint file to use;
                if not specified, the file "blueprint.yaml" will be used, if it exists'''
_CONF_DESC = '''specify the configuration to use;
                if not specified, the configuration "default" will be used, if it exists'''

def parse_args() -> dict:
    """
    Parse the command line's arguments.

    :returns: A dictionary of options passed to the script, distributed in groups.

    :raises SystemExit: No arguments or wrong ones were provided.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='codestacker')
    sub_parser = parser.add_subparsers(dest='command')

    parser.add_argument('-f', dest='file', default='blueprint.yaml', help=_FILE_DESC)
    parser.add_argument('-c', dest='config', default='default', help=_CONF_DESC)

    # 'clean' argument.
    sub_parser.add_parser('clean', help='clean the compilation results')

    # 'build' argument.
    sub_parser.add_parser('build', help='trigger the build process')

    # Parse the arguments.
    # May abort the script if unexpected arguments were passed.
    args = parser.parse_args()

    # If no arguments were provided, print only the script's usage and exit.
    if not len(sys.argv) > 1:
        parser.print_usage()
        sys.exit(0)

    return vars(args)
