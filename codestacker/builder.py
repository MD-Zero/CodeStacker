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
    from .constants         import keys as K
    from .logger            import Logger
    from .sources_inspector import validate_sources

    Logger.begin('Start build')

    validate_sources(config[K.INCLUDE], config[K.SOURCES])

    _compile(config)
    _link(config)

    Logger.end('Build successful')

####################################################################################################

_SPECIAL_FLAG = '-fdiagnostics-color=always'

def _compile(config):
    """
    Compile the source files into object files.
    """
    import os
    import re
    import subprocess

    from .constants  import errors as E, keys as K
    from .exceptions import TechnicalError
    from .logger     import Logger

    files_to_compile = _get_files_to_recompile(config)

    if not files_to_compile:
        Logger.info('Nothing to (re)compile')
        return

    Logger.begin('Compilation')

    # Step 1: compiler.
    compile_command = ['g++']

    # Step 2: compilation flags.
    compile_command.extend(config[K.FLAGS])

    # Add this special flag to force the compiler to print its output in colors.
    if _SPECIAL_FLAG not in compile_command:
        compile_command.append(_SPECIAL_FLAG)

    # Step 3: include directory.
    compile_command.extend(['-I', config[K.INCLUDE]])

    for file in files_to_compile:
        Logger.info('Compiling {}...'.format(os.path.relpath(file, config[K.ROOT])))

        # Step 4: source file to compile.
        file_to_compile = ['-c', file]

        target_filename = re.sub(r'.cpp$', '.o', os.path.basename(file))

        # Step 5: object file to produce.
        file_to_compile.extend(['-o', os.path.join(config[K.BUILD], target_filename)])

        try:
            subprocess.run([*compile_command, *file_to_compile], stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(E.COMPILATION_FAILED, error.stderr.decode('UTF-8'))

    Logger.end('Compilation successful')

####################################################################################################

def _get_files_to_recompile(config) -> set:
    """
    Return a list of source files that, given the existing object files in the "build" folder, need
    to be (re)compiled.
    """
    import os
    import subprocess

    from .constants   import errors as E, keys as K
    from .exceptions  import TechnicalError
    from .file_system import get_files

    obj_timestamp = {}

    for file in get_files(config[K.BUILD], '.o'):
        obj_timestamp[os.path.basename(file)] = os.path.getmtime(file)

    recipes = {}
    output = ''
    preproc_command = ['g++', '-I', config[K.INCLUDE], '-MM']

    for file in get_files(config[K.SOURCES], '.cpp'):
        try:
            output = subprocess.run([*preproc_command, file], stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(E.RECIPE_FAILED, error.stderr.decode('UTF-8'))

        target, prerequisites = output.stdout.decode('UTF-8').split(':', 1)

        prerequisites = prerequisites.replace('\\', '').split()

        recipes[target] = {source: os.path.getmtime(source) for source in prerequisites}

    to_compile = set()

    for obj, file_timestamp in recipes.items():
        # Case 1: new targets.
        if obj not in obj_timestamp:
            to_compile.update(file_timestamp.keys())
        # Case 2: modified source files.
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

    from .constants   import errors as E, keys as K
    from .exceptions  import TechnicalError
    from .file_system import get_files
    from .logger      import Logger

    Logger.begin('Linking')

    # Step 1: compiler.
    linking_command = ['g++']

    # Step 2, 3: output executable and object files.
    linking_command.extend(['-o', os.path.join(config[K.BINARY], config[K.OUTPUT])])
    linking_command.extend(get_files(config[K.BUILD], '.o'))

    # Step 4: libraries.
    if config[K.LIBRARIES]:
        linking_command.extend('-l' + x for x in config[K.LIBRARIES])

    try:
        subprocess.run(linking_command, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as error:
        raise TechnicalError(E.LINKING_FAILED, error.stderr.decode('UTF-8'))

    Logger.end('Linking successful')
