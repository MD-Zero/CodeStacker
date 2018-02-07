#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code builder (compilation + linking).
"""

####################################################################################################

def build(dir_root, config):
    """
    Build the project (compile + link).
    """
    import os

    _compile(os.path.realpath(os.path.dirname(dir_root)), config)
    _link(config)

####################################################################################################

def _compile(dir_root, config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .        import constants as keys
    from .helpers import print_and_die
    from .logger  import log_info, log_ok

    _normalize_paths(dir_root, config)

    # Dereferenced for performance.
    dir_include = config[keys.KEY_DIR_INCLUDE]
    compiler_options = config[keys.KEY_COMPILER_OPTIONS]

    os.chdir(config[keys.KEY_DIR_BUILD])

    log_info('>> Start compilation')

    for source in _get_files(config[keys.KEY_DIR_SOURCE], '.cpp'):
        location = os.path.relpath(source, dir_root)

        try:
            log_info('Compiling {}...'.format(location))

            subprocess.check_output([
                'g++', *compiler_options,
                '-I', dir_include,
                '-c', source])
        except subprocess.CalledProcessError:
            print_and_die('{} compilation failed'.format(location))

    log_ok('<< Compilation successful')

####################################################################################################

def _link(config):
    """
    Link the object files into an executable.
    """
    import os
    import subprocess

    from .        import constants as keys
    from .helpers import print_and_die
    from .logger  import log_info, log_ok

    os.chdir(config[keys.KEY_DIR_BIN])

    try:
        log_info('Linking...')

        subprocess.check_output([
            'g++', '-o', config[keys.KEY_OUTPUT],
            *_get_files(config[keys.KEY_DIR_BUILD], '.o')])
    except subprocess.CalledProcessError:
        print_and_die('Linking failed')

    log_ok('<< Linking successful')

####################################################################################################

def _normalize_paths(dir_root, config):
    """
    Normalize directories with absolute paths, and create optional missing directories.
    """
    import os

    from . import constants as keys

    # "dir_include" (mandatory).
    config[keys.KEY_DIR_INCLUDE] =\
        os.path.realpath(os.path.join(dir_root, config[keys.KEY_DIR_INCLUDE]))

    _check_existence(dir_root, config[keys.KEY_DIR_INCLUDE])

    # "dir_source" (mandatory).
    config[keys.KEY_DIR_SOURCE] =\
        os.path.realpath(os.path.join(dir_root, config[keys.KEY_DIR_SOURCE]))

    _check_existence(dir_root, config[keys.KEY_DIR_SOURCE])

    # "dir_bin" (optional).
    if keys.KEY_DIR_BIN not in config:
        config[keys.KEY_DIR_BIN] = os.path.realpath(os.path.join(dir_root, 'bin'))
    else:
        config[keys.KEY_DIR_BIN] =\
            os.path.realpath(os.path.join(dir_root, config[keys.KEY_DIR_BIN]))

    _check_existence(dir_root, config[keys.KEY_DIR_BIN], True)

    # "dir_build" (optional).
    if keys.KEY_DIR_BUILD not in config:
        config[keys.KEY_DIR_BUILD] = os.path.realpath(os.path.join(dir_root, 'build'))
    else:
        config[keys.KEY_DIR_BUILD] =\
            os.path.realpath(os.path.join(dir_root, config[keys.KEY_DIR_BUILD]))

    _check_existence(dir_root, config[keys.KEY_DIR_BUILD], True)

####################################################################################################

def _check_existence(dir_root, directory, should_create=False):
    """
    Check whether the directory in input exists or not, and optionally create it.
    """
    import os

    from .helpers import print_and_die

    if not os.path.exists(directory):
        if should_create:
            os.makedirs(directory)
        else:
            print_and_die(
                'Directory "{}" does not exist'.format(os.path.relpath(directory, dir_root)))

####################################################################################################

def _get_files(directory, extension):
    """
    Gather all the files ending with "extension" in the given directory--and descendants.
    """
    import os

    from .helpers import print_and_die

    all_sources = []

    for current_dir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                all_sources.append(os.path.join(current_dir, file))

    if not all_sources:
        print_and_die('No sources to compile')

    return all_sources
