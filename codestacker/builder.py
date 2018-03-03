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
    from .                  import keys
    from .logger            import Logger
    from .sources_inspector import validate_sources

    Logger.begin('Start build')

    validate_sources(config[keys.INCLUDE], config[keys.SOURCES])

    _compile(config)
    _link(config)

    Logger.end('Build successful')

####################################################################################################

_ERROR_COMPILATION = 'compilation failed'

def _compile(config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .              import keys
    from .cache_builder import get_files_to_compile
    from .exceptions    import TechnicalError
    from .logger        import Logger

    files_to_compile = get_files_to_compile(config)

    if not files_to_compile:
        Logger.info('Nothing to (re)compile')

        return

    Logger.begin('Compilation')

    # Dereferenced for performance.
    root = config[keys.ROOT]

    compile_command = ['g++']

    if keys.FLAGS in config:
        compile_command.extend(config[keys.FLAGS])

    compile_command.extend(['-I', config[keys.INCLUDE]])

    os.chdir(config[keys.BUILD])

    for file in files_to_compile:
        Logger.info('Compiling {}...'.format(os.path.relpath(file, root)))

        compile_command.extend(['-c', file])

        try:
            subprocess.run(compile_command, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(_ERROR_COMPILATION, error.stderr.decode('UTF-8'))

    os.chdir(root)

    Logger.end('Compilation successful')

####################################################################################################

_ERROR_LINKING = 'linking failed'

def _link(config):
    """
    Link the object files into an executable.
    """
    import os
    import subprocess

    from .            import keys
    from .exceptions  import TechnicalError
    from .file_system import get_files
    from .logger      import Logger

    Logger.begin('Linking')

    os.chdir(config[keys.BINARY])

    linking_command = ['g++', '-o', config[keys.OUTPUT], *get_files(config[keys.BUILD], '.o')]

    if config[keys.LIBRARIES]:
        linking_command.extend('-l' + x for x in config[keys.LIBRARIES])

    try:
        subprocess.run(linking_command, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as error:
        raise TechnicalError(_ERROR_LINKING, error.stderr.decode('UTF-8'))

    os.chdir(config[keys.ROOT])

    Logger.end('Linking successful')
