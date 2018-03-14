#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Argument parsing utility.
"""

####################################################################################################

_DEFAULT_FILE = 'blueprint.yaml'
_DEFAULT_CONFIG = 'default'

_FILE_DESC = '''specify the blueprint file to use; if not specified, the file "{}" will be used, if
                it exists'''.format(_DEFAULT_FILE)
_CONF_DESC = '''specify the configuration to use; if not specified, the configuration "{}" will be
                used, if it exists'''.format(_DEFAULT_CONFIG)

def parse_args():
    """
    Parse the command line's arguments.

    :returns: A dictionary of options passed to the script, distributed in groups.

    :raises SystemExit: no arguments or wrong ones were provided.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='codestacker')
    sub_parser = parser.add_subparsers(dest='command')

    parser.add_argument('-f', dest='file', default=_DEFAULT_FILE, help=_FILE_DESC)
    parser.add_argument('-c', dest='config', default=_DEFAULT_CONFIG, help=_CONF_DESC)

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
