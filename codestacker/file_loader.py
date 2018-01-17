#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File loading utility.
"""

def load_yaml(file):
    """
    Read a YAML file and return its content as a dictionary--or die.
    """
    import yaml

    from .helpers import print_and_die

    yaml_content = None

    try:
        with open(file, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)
    except IOError as error:
        print_and_die('File I/O', error)
    except yaml.YAMLError as error:
        print_and_die('YAML parsing error', error)
    else:
        return yaml_content
