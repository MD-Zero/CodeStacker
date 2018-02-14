#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File loading utility.
"""

####################################################################################################

def load_yaml(file):
    """
    Read a YAML file and return its content as a list of dictionaries--or die.
    """
    import yaml

    from .helpers import die
    from .logger  import log_ok, log_info

    log_info('>> Reading "{}" file...'.format(file))

    content = []

    # Try to load the file's content.
    try:
        with open(file, 'r') as stream:
            content = list(yaml.safe_load_all(stream))
    except IOError as error:
        die('File I/O', error)
    except yaml.YAMLError as error:
        die('YAML loading error', error)

    if not content:
        die('Empty YAML file')

    log_ok('<< Success')

    return content
