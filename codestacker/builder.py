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

def _compile(config):
    """
    Compile the source files into object files.
    """
    import os
    import subprocess

    from .           import errors as E
    from .           import keys
    from .exceptions import TechnicalError
    from .logger     import Logger

    files_to_compile = _get_files_to_recompile(config)

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
            raise TechnicalError(E.COMPILATION_FAILED, error.stderr.decode('UTF-8'))

    os.chdir(root)

    Logger.end('Compilation successful')

####################################################################################################

def _get_files_to_recompile(config):
    """
    Return a list of source files that, given the existing object files in the "build" folder, need
    to be (re)compiled.
    """
    import os
    import subprocess

    from .            import errors as E
    from .            import keys
    from .exceptions  import TechnicalError
    from .file_system import get_files

    obj_timestamp = {}

    for file in get_files(config[keys.BUILD], '.o'):
        obj_timestamp[os.path.basename(file)] = os.path.getmtime(file)

    recipes = {}

    for file in get_files(config[keys.SOURCES], '.cpp'):
        command = ['g++', '-I', config[keys.INCLUDE], '-MM', file]
        recipe = ''

        try:
            recipe = subprocess.run(command, stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(E.RECIPE_FAILED, error.stderr.decode('UTF-8'))

        target, prerequisites = recipe.stdout.decode('UTF-8').split(':', 1)

        prerequisites = prerequisites.replace('\\', '').split()

        recipes[target] = {source: os.path.getmtime(source) for source in prerequisites}

    to_compile = set()

    for obj, file_timestamp in recipes.items():
        # New targets.
        if obj not in obj_timestamp:
            to_compile.update(file_timestamp.keys())
        # Modified source files.
        else:
            for file, timestamp in file_timestamp.items():
                if timestamp > obj_timestamp[obj]:
                    to_compile.add(file)

    to_compile = set(file for file in to_compile if file.endswith('.cpp'))

    return to_compile

####################################################################################################

def _link(config):
    """
    Link the object files into an executable.
    """
    import os
    import subprocess

    from .            import errors as E
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
        raise TechnicalError(E.LINKING_FAILED, error.stderr.decode('UTF-8'))

    os.chdir(config[keys.ROOT])

    Logger.end('Linking successful')
