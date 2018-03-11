#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File utilities.
"""

####################################################################################################

def get_files(directory, extension):
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

def check_files(directory, extension):
    """
    Check the validity of any source files within directory and descendants.

    :param directory: The directory to start visiting from.
    :param extension: The extension to look for in the directory and descendants.

    :raises FileSystemError: a file doesn't match the naming requirements.
    """
    import os
    import re

    from codestacker.errors            import errors as E
    from codestacker.errors.exceptions import FileSystemError

    pattern = re.compile(r'^\w+$')

    for current_dir, dirs, files in os.walk(directory):
        for file in files:
            if (file.endswith(extension)) and (pattern.search(os.path.splitext(file)[0]) is None):
                raise FileSystemError(E.INVALID_FILENAME, file)
