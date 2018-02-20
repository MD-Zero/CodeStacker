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
    import os

    from .exceptions import TechnicalError

    abs_path = os.path.realpath(os.path.join(root, directory))

    if not os.path.exists(abs_path):
        raise TechnicalError('file "{}" is nonexistent'.format(abs_path))

    return abs_path

####################################################################################################

def get_files(directory, extension):
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
