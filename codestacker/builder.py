#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code builder (compilation + linking).
"""

####################################################################################################

def compile_sources(dir_project, config):
    """
    TODO
    """
    import os
    import subprocess

    from .       import constants as keys
    from .logger import log_info, log_ok

    # Directory in blueprint file must be declared relatively to it.
    dir_include = config[keys.KEY_DIR_INCLUDE]
    dir_source = config[keys.KEY_DIR_SOURCE]

    _check_existence(dir_include, dir_source)

    dir_bin = config[keys.KEY_DIR_BIN]
    dir_build = config[keys.KEY_DIR_BUILD]

    if not os.path.exists(dir_build):
        os.makedirs(dir_build)

    os.chdir(dir_build)

    all_sources = _get_sources(dir_source)

    log_info('>> Start compilation')

    for source in all_sources:
        try:
            log_info('Compiling {}...'.format(os.path.basename(source)))

            subprocess.run([
                'g++', *config[keys.KEY_COMPILER_OPTIONS],
                '-I', dir_include,
                '-c', source])
        except subprocess.CalledProcessError as error:
            raise error

    log_ok('<< Compilation successful')

####################################################################################################

def link_objects():
    """
    """
    pass

####################################################################################################

def _check_existence(*dirs):
    """
    Check whether the directories in input exist or not.
    """
    import os

    from .helpers import print_and_die

    for directory in dirs:
        if not os.path.exists(directory):
            print_and_die('Directory "{}" does not exist'.format(directory))

####################################################################################################

def _get_sources(dir_source):
    """
    Gather all the "*.cpp" source files in the given directory and descendants.
    """
    import os

    all_sources = []

    for root, dirs, files in os.walk(dir_source):
        for file in files:
            if file.endswith('.cpp'):
                all_sources.append(os.path.join(root, file))

    return all_sources
