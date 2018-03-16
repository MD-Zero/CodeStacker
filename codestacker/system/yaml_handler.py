#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML file handling utilities.
"""

####################################################################################################

def load_yaml(file):
    """
    Read a YAML file and return its content.

    :param file: The filename / path to read from.

    :returns: The file's content as a list of dictionaries.

    :raises FileSystemError: the file reading failed.
    :raises TechnicalError: the YAML parsing failed, or the file is empty.
    """
    import os
    import yaml

    from codestacker.errors            import errors
    from codestacker.errors.exceptions import FileSystemError, TechnicalError
    from codestacker.logger            import Logger

    Logger.begin('Load "{}" file...'.format(os.path.relpath(file)))

    content = []

    try:
        with open(file, 'r') as stream:
            content = list(yaml.safe_load_all(stream))
    except IOError as error:
        raise FileSystemError(errors.FILE_READING, error=error)
    except yaml.YAMLError as error:
        raise TechnicalError(errors.YAML_PARSING, error=error)

    if not content:
        raise TechnicalError(errors.EMPTY_YAML)

    # Transform the "list of dicts" into one single dict.
    content = {key: value for pair in content for key, value in pair.items()}

    Logger.end('Success')

    return content

####################################################################################################

def dump_yaml(content, file):
    """
    Dump some YAML content into a file.

    :param content: The dictionary to write, in a form of YAML structure(s), in a file.
    :param file: The filename / path to write in.
    """
    import yaml

    from codestacker.errors            import errors
    from codestacker.errors.exceptions import TechnicalError

    try:
        with open(file, 'w') as stream:
            yaml.safe_dump(content, stream, default_flow_style=False)
    except IOError as error:
        TechnicalError(errors.FILE_WRITING, error).print()
    except yaml.YAMLError as error:
        TechnicalError(errors.YAML_DUMPING, error).print()
