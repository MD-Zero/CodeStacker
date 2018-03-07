#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File utilities.
"""

####################################################################################################

def get_files(directory, extension) -> list:
    """
    Browse a directory and descendants, and gather all files ending with a given extension.

    :param directory: The directory to start visiting from.
    :param extension: The extension to look for in the directory and descendants.

    :returns: A list of filenames / paths.
    """
    import os

    all_files = []

    for current_dir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                all_files.append(os.path.join(current_dir, file))

    return all_files

####################################################################################################

def check_files(directory, file_extension):
    """
    Check the validity of any source files within directory and descendants.

    :param directory: The directory to start visiting from.
    :param extension: The extension to look for in the directory and descendants.

    :raises FileSystemError: A file doesn't match the naming requirements.
    """
    import os
    import re

    from codestacker.constants  import errors as E
    from codestacker.exceptions import TechnicalError

    for file in get_files(directory, file_extension):
        filename = os.path.basename(file)

        if re.search(r'^\w+{}$'.format(file_extension), filename) is None:
            raise TechnicalError(E.INVALID_FILENAME.format(filename))
