#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File loading utility.
"""

####################################################################################################

def load_yaml(file):
    """
    Read a YAML file and return its content as a dictionary--or die.
    """
    import yaml

    from .helpers import print_and_die

    config = None

    try:
        with open(file, 'r') as stream:
            config = list(yaml.safe_load_all(stream))
    except IOError as error:
        print_and_die('File I/O', error)
    except yaml.YAMLError as error:
        print_and_die('YAML parsing error', error)

    if config is None:
        print_and_die('Empty configuration file')

    return config
