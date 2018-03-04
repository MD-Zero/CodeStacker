#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File handling utility.
"""

####################################################################################################

def load_yaml(file):
    """
    Read a YAML file and return its content as a list of dictionaries.
    """
    import os
    import yaml

    from .           import errors as E
    from .exceptions import TechnicalError
    from .logger     import Logger

    Logger.begin('Reading "{}" file...'.format(os.path.relpath(file)))

    content = []

    # Try to load the file's content.
    try:
        with open(file, 'r') as stream:
            content = list(yaml.safe_load_all(stream))
    except IOError as error:
        raise TechnicalError(E.FILE_READING, error)
    except yaml.YAMLError as error:
        raise TechnicalError(E.YAML_PARSING, error)

    if not content:
        raise TechnicalError(E.EMPTY_YAML)

    # Transform the "list of dicts" into one single dict.
    content = {key: value for pair in content for key, value in pair.items()}

    Logger.end('Success')

    return content

####################################################################################################

def dump_yaml(content, file):
    """
    Dump some YAML content into a file.
    """
    import yaml

    from .           import errors as E
    from .exceptions import TechnicalError

    try:
        with open(file, 'w') as stream:
            yaml.safe_dump(content, stream, default_flow_style=False)
    except IOError as error:
        TechnicalError(E.FILE_WRITING, error).print()
    except yaml.YAMLError as error:
        TechnicalError(E.YAML_DUMPING, error).print()
