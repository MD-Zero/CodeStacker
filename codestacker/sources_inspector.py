#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sources inspector module: validate the correctness of source files.
"""

####################################################################################################

def validate_sources(include_dir, sources_dir):
    """
    Check if headers and sources filenames are valid.
    """
    from .logger import Logger

    Logger.begin('Checking headers and sources...')

    _check_directory(include_dir, '.hpp')
    _check_directory(sources_dir, '.cpp')

    Logger.end('Headers and sources valid')

####################################################################################################

_ERROR_INVALID_FILE = 'file "{}" doesn\'t match filenames requirements'

def _check_directory(directory, file_extension):
    """
    Check the directory's content, for all files ending with "file_extension".
    """
    import os
    import re

    from .exceptions  import TechnicalError
    from .file_system import get_files

    for file in get_files(directory, file_extension):
        filename = os.path.basename(file)

        if re.search(r'^\w+{}$'.format(file_extension), filename) is None:
            raise TechnicalError(_ERROR_INVALID_FILE.format(filename))
