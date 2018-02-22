#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File loading utility.
"""

####################################################################################################

_ERROR_FILE_READING = 'file reading error'
_ERROR_YAML_PARSING = 'YAML parsing error'
_ERROR_EMPTY_FILE = 'empty YAML file'

def load_yaml(file):
    """
    Read a YAML file and return its content as a list of dictionaries.
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
        raise TechnicalError(_ERROR_FILE_READING, error)
    except yaml.YAMLError as error:
        raise TechnicalError(_ERROR_YAML_PARSING, error)

    if not content:
        raise TechnicalError(_ERROR_EMPTY_FILE)

    # Transform the "list of dictionaries" into one single dictionary.
    content = {key: value for pair in content for key, value in pair.items()}

    log_ok('<< Success')

    return content

####################################################################################################

_ERROR_FILE_WRITING = 'file writing error'
_ERROR_YAML_DUMPING = 'YAML dumping error'

def dump_yaml(content, file):
    """
    Dump some YAML content into a file.
    """
    import yaml

    from .exceptions import TechnicalError

    try:
        with open(file, 'w') as stream:
            yaml.safe_dump(content, stream)
    except IOError as error:
        TechnicalError(_ERROR_FILE_WRITING, error).print()
    except yaml.YAMLError as error:
        TechnicalError(_ERROR_YAML_DUMPING, error).print()
