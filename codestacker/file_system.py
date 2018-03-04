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
