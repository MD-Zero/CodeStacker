#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File system utilities.
"""

####################################################################################################

def get_absolute_path(root, directory):
    """
    Return the absolute path from the concatenated pair {root, directory} in input.
    """
    import errno
    import os

    from .exceptions import TechnicalError

    new_path = os.path.realpath(os.path.join(root, directory))

    if not os.path.exists(new_path):
        raise TechnicalError('', FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), new_path))

    return new_path

####################################################################################################

def get_files_with_extension(directory, extension):
    """
    Gather all the files ending with "extension" in the given directory and descendants.
    """
    import os

    all_files = []

    for current_dir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                all_files.append(os.path.join(current_dir, file))

    return all_files
