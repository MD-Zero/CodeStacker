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
    from .logger import log_info, log_ok

    log_info('>> Start build')

    if _compile(config):
        _link(config)

    log_ok('<< Build successful')

####################################################################################################

_ERROR_COMPILATION_FAILED = '{} compilation failed'

def _compile(config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .              import keys
    from .cache_builder import get_files_to_compile
    from .exceptions    import TechnicalError
    from .file_system   import get_files
    from .logger        import log_info, log_ok

    should_link = True
    files_to_compile = get_files_to_compile(config)

    if not files_to_compile:
        log_info('Nothing to (re)compile')

        should_link = False

        return should_link

    log_info('>> Compilation')

    # Dereferenced for performance.
    root = config[keys.ROOT]

    os.chdir(config[keys.BUILD])

    compile_command = ['g++']

    if keys.FLAGS in config:
        compile_command.extend(config[keys.FLAGS])

    compile_command.extend(['-I', config[keys.INCLUDE]])

    for file in files_to_compile:
        relative_file = os.path.relpath(file, root)

        log_info('Compiling {}...'.format(relative_file))

        compile_command.extend(['-c', file])

        try:
            subprocess.check_output(compile_command)
        except subprocess.CalledProcessError:
            raise TechnicalError(_ERROR_COMPILATION_FAILED.format(relative_file))

    os.chdir(root)

    log_ok('<< Compilation successful')

    return should_link

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

    log_info('>> Linking')

    os.chdir(config[keys.BINARY])

    linking_command = ['g++', '-o', config[keys.OUTPUT], *get_files(config[keys.BUILD], '.o')]

    try:
        subprocess.check_output(linking_command)
    except subprocess.CalledProcessError:
        raise TechnicalError('linking failed')

    os.chdir(config[keys.ROOT])

    log_ok('<< Linking successful')
