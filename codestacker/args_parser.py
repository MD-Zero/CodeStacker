#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Argument parsing utility.
"""

DEFAULT_CONFIG_FILE = 'blueprint.yaml'

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
        default=DEFAULT_CONFIG_FILE, help='specify the configuration file to use')

    # 'compilation mode' arguments.
    mode_group = parser_build.add_mutually_exclusive_group(required=True)

    mode_group.add_argument(
        '-R', '--release',
        action='store_true', help='build in "release" mode')

    mode_group.add_argument(
        '-D', '--debug',
        action='store_true', help='build in "debug" mode')

    # Parse the arguments.
    # May abort the script if unexpected arguments were passed.
    args = parser.parse_args()

    # If no arguments were provided, print only the script's usage and exit.
    if not len(sys.argv) > 1:
        parser.print_usage()
        sys.exit()

    return vars(args)
