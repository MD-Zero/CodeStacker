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
    import os
    import yaml

    from .exceptions import TechnicalError
    from .logger     import log_ok, log_info

    log_info('>> Reading "{}" file...'.format(os.path.relpath(file)))

    content = []

    # Try to load the file's content.
    try:
        with open(file, 'r') as stream:
            content = list(yaml.safe_load_all(stream))
    except IOError as error:
        raise TechnicalError('file handling error', error)
    except yaml.YAMLError as error:
        raise TechnicalError('YAML parsing error', error)

    if not content:
        raise TechnicalError('empty YAML file')

    log_ok('<< Success')

    return content
