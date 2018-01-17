#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File loading utility.
"""

def load_yaml(file):
    """
    Read a YAML file and return its content as a dictionary.
    """
    import yaml

    yaml_content = None

    try:
        with open(file, 'r') as yaml_file:
            yaml_content = yaml.safe_load(yaml_file)
    except IOError as error:
        print(error)
        sys.exit()
    except yaml.YAMLError as error:
        print('YAML parsing error:', error)
        sys.exit()
    else:
        return yaml_content
