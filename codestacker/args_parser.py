#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Argument parsing utility.
"""

_DEFAULT_CONFIG_FILE = 'blueprint.yaml'
_DEFAULT_PROFILE = 'Default'

####################################################################################################

def parse_args():
    """
    Parse the command line's arguments.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='codestacker')

    # 'build' arguments.
    parser_build = parser.add_subparsers().add_parser(
        'build',
        help='trigger the build process')

    parser_build.add_argument(
        '-f', '--file',
        default=_DEFAULT_CONFIG_FILE, help='specify the configuration file to use')

    parser_build.add_argument(
        '-p', '--profile',
        default=_DEFAULT_PROFILE, help='specify the profile to use from the configuration file')

    # Parse the arguments.
    # May abort the script if unexpected arguments were passed.
    args = parser.parse_args()

    # If no arguments were provided, print only the script's usage and exit.
    if not len(sys.argv) > 1:
        parser.print_usage()
        sys.exit()

    return vars(args)
