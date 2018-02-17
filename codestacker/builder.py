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

    _compile(os.path.realpath(dir_root), config)
    _link(config)

####################################################################################################

def _compile(dir_root, config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .            import constants as keys
    from .file_system import get_absolute_path, get_files_with_extension
    from .helpers     import die
    from .logger      import log_info, log_ok

    # Dereferenced for performance.
    dir_include = config[keys.KEY_DIR_INCLUDE]
    compiler_options = config[keys.KEY_COMPILER_OPTIONS]

    os.chdir(config[keys.KEY_DIR_BUILD])

    log_info('>> Compilation')

    for source in get_files_with_extension(config[keys.KEY_DIR_SOURCE], '.cpp'):
        location = os.path.relpath(source, dir_root)

        try:
            log_info('Compiling {}...'.format(location))

            subprocess.check_output([
                'g++', *compiler_options,
                '-I', dir_include,
                '-c', source])
        except subprocess.CalledProcessError:
            die('{} compilation failed'.format(location))

    os.chdir(dir_root)

    log_ok('<< Compilation successful')

####################################################################################################

def _link(config):
    """
    Link the object files into an executable.
    """
    import os
    import subprocess

    from .            import constants as keys
    from .file_system import get_files_with_extension
    from .helpers     import die
    from .logger      import log_info, log_ok

    os.chdir(config[keys.KEY_DIR_BIN])

    try:
        log_info('>> Linking')

        subprocess.check_output([
            'g++', '-o', config[keys.KEY_OUTPUT],
            *get_files_with_extension(config[keys.KEY_DIR_BUILD], '.o')])
    except subprocess.CalledProcessError:
        die('Linking failed')

    log_ok('<< Linking successful')
