#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sources inspector module: validate the correctness of source files.
"""

####################################################################################################

_ERROR_INVALID_FILE = 'file "{}" doesn\'t match filenames requirements'

def validate_sources(include_dir, sources_dir):
    """
    Check if headers and sources filename is a valid one.
    """
    import os
    import re

    from .exceptions  import TechnicalError
    from .file_system import get_files
    from .logger      import Logger

    Logger.begin('Checking headers and sources...')

    # Headers.
    for file in get_files(include_dir, '.hpp'):
        filename = os.path.basename(file)

        if re.search(r'^\w+\.hpp$', filename) is None:
            raise TechnicalError(_ERROR_INVALID_FILE.format(filename))

    # Sources.
    for file in get_files(include_dir, '.cpp'):
        filename = os.path.basename(file)

        if re.search(r'^\w+\.cpp$', filename) is None:
            raise TechnicalError(_ERROR_INVALID_FILE.format(filename))

    Logger.end('Headers and sources valid')
