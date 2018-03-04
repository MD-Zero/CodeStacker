#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File system utilities.
"""

####################################################################################################

def get_files(directory, extension) -> list:
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

####################################################################################################

def validate_sources(include_dir, sources_dir):
    """
    Check if headers and sources filenames are valid.
    """
    from codestacker.logger import Logger

    Logger.begin('Checking headers and sources...')

    _check_directory(include_dir, '.hpp')
    _check_directory(sources_dir, '.cpp')

    Logger.end('Headers and sources valid')

####################################################################################################

def _check_directory(directory, file_extension):
    """
    Check the directory's content, for all files ending with "file_extension".
    """
    import os
    import re

    from codestacker.constants  import errors as E
    from codestacker.exceptions import TechnicalError

    for file in get_files(directory, file_extension):
        filename = os.path.basename(file)

        if re.search(r'^\w+{}$'.format(file_extension), filename) is None:
            raise TechnicalError(E.INVALID_FILENAME.format(filename))
