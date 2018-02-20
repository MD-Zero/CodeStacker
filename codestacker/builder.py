#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code builder: compilation + linking.
"""

####################################################################################################

def build(dir_root, config):
    """
    Build the project (compile + link).
    """
    _compile(dir_root, config)
    _link(config)

####################################################################################################

def _compile(dir_root, config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .            import constants
    from .exceptions  import TechnicalError
    from .file_system import get_absolute_path, get_files_with_extension
    from .logger      import log_info, log_ok

    # Dereferenced for performance.
    dir_include = config[constants.KEY_DIR_INCLUDE]

    os.chdir(config[constants.KEY_DIR_BUILD])

    log_info('>> Compilation')

    compile_command = 'g++'

    if constants.KEY_COMPILER_OPTIONS in config:
        compile_command += ' ' + ' '.join(config[constants.KEY_COMPILER_OPTIONS])

    compile_command += ' -I {}'.format(dir_include)

    for source in get_files_with_extension(config[constants.KEY_DIR_SOURCE], '.cpp'):
        location = os.path.relpath(source, dir_root)

        try:
            log_info('Compiling {}...'.format(location))

            compile_command += ' -c {}'.format(source)

            subprocess.check_output(compile_command.split())
        except subprocess.CalledProcessError:
            raise TechnicalError('{} compilation failed'.format(location))

    os.chdir(dir_root)

    log_ok('<< Compilation successful')

####################################################################################################

def _link(config):
    """
    Link the object files into an executable.
    """
    import os
    import subprocess

    from .            import constants
    from .exceptions  import TechnicalError
    from .file_system import get_files_with_extension
    from .logger      import log_info, log_ok

    os.chdir(config[constants.KEY_DIR_BIN])

    try:
        log_info('>> Linking')

        subprocess.check_output([
            'g++', '-o', config[constants.KEY_OUTPUT],
            *get_files_with_extension(config[constants.KEY_DIR_BUILD], '.o')])
    except subprocess.CalledProcessError:
        raise TechnicalError('linking failed')

    log_ok('<< Linking successful')
