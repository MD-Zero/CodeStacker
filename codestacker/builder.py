#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code builder: compilation + linking.
"""

####################################################################################################

def build(config):
    """
    Build the project (compile + link).
    """
    _compile(config)
    _link(config)

####################################################################################################

_ERROR_COMPILATION_FAILED = '{} compilation failed'

def _compile(config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .            import keys
    from .exceptions  import TechnicalError
    from .file_system import get_files
    from .logger      import log_info, log_ok

    log_info('>> Compilation')

    # Dereferenced for performance.
    root = config[keys.ROOT]

    os.chdir(config[keys.BUILD])

    compile_command = ['g++']

    if keys.FLAGS in config:
        compile_command.extend(config[keys.FLAGS])

    compile_command.extend(['-I', config[keys.INCLUDE]])

    for file in get_files(config[keys.SOURCES], '.cpp'):
        relative_file = os.path.relpath(file, root)

        log_info('Compiling {}...'.format(relative_file))

        compile_command.extend(['-c', file])

        try:
            subprocess.check_output(compile_command)
        except subprocess.CalledProcessError:
            raise TechnicalError(_ERROR_COMPILATION_FAILED.format(relative_file))

    os.chdir(root)

    log_ok('<< Compilation successful')

####################################################################################################

def _link(config):
    """
    Link the object files into an executable.
    """
    import os
    import subprocess

    from .            import keys
    from .exceptions  import TechnicalError
    from .file_system import get_files
    from .logger      import log_info, log_ok

    os.chdir(config[keys.BINARY])

    linking_command = ['g++', '-o', config[keys.OUTPUT], *get_files(config[keys.BUILD], '.o')]

    try:
        log_info('>> Linking')

        subprocess.check_output(linking_command)
    except subprocess.CalledProcessError:
        raise TechnicalError('linking failed')

    os.chdir(config[keys.ROOT])

    log_ok('<< Linking successful')
