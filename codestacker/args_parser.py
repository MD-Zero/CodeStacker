#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Argument parsing utility.
"""

####################################################################################################

def parse_args():
    """
    Parse the command line's arguments, and return its content as a dictionary.
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
        default='blueprint.yaml', help='specify the blueprint file to use')

    parser_build.add_argument(
        '-c', '--config',
        default='default', help='specify the configuration to use')

    # Parse the arguments.
    # May abort the script if unexpected arguments were passed.
    args = parser.parse_args()

    # If no arguments were provided, print only the script's usage and exit.
    if not len(sys.argv) > 1:
        parser.print_usage()
        sys.exit(0)

    return vars(args)
