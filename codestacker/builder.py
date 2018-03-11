#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code builder: compilation + linking.
"""

####################################################################################################

def build(config):
    """
    Build the project (compile + link).

    :param config: The configuration to operate on.
    """
    from .logger import Logger

    Logger.begin('Start build')

    _validate_sources(config)
    _compile(config)
    _link(config)

    Logger.end('Build successful')

####################################################################################################

def _validate_sources(config):
    """
    Check if headers and sources filenames are valid.

    :param config: The configuration to operate on.
    """
    from .constants             import keys
    from .logger                import Logger
    from .system.file_utilities import check_files

    Logger.begin('Checking headers and sources...')

    check_files(config[keys.INCLUDE], '.hpp')
    check_files(config[keys.SOURCES], '.cpp')

    Logger.end('Headers and sources valid')

####################################################################################################

_SPECIAL_FLAG = '-fdiagnostics-color=always'

def _compile(config):
    """
    Compile the source files into object files.

    :param config: The configuration to operate on.

    :raises TechnicalError: a source file compilation failed.
    """
    import os
    import re
    import subprocess

    from .constants         import keys
    from .errors            import errors
    from .errors.exceptions import TechnicalError
    from .logger            import Logger

    files_to_compile = _get_files_to_recompile(config)

    if not files_to_compile:
        Logger.info('Nothing to (re)compile')
        return

    Logger.begin('Compilation')

    # Step 1: compiler.
    compile_command = ['g++']

    # Step 2: compilation flags.
    compile_command.extend(config[keys.FLAGS])

    # Add this special flag to force the compiler to print its output in colors.
    if _SPECIAL_FLAG not in compile_command:
        compile_command.append(_SPECIAL_FLAG)

    # Step 3: include directory.
    compile_command.extend(['-I', config[keys.INCLUDE]])

    for file in files_to_compile:
        Logger.info('Compiling {}...'.format(os.path.relpath(file, config[keys.ROOT])))

        # Step 4: source file to compile.
        file_to_compile = ['-c', file]

        target_filename = re.sub(r'.cpp$', '.o', os.path.basename(file))

        # Step 5: object file to produce.
        file_to_compile.extend(['-o', os.path.join(config[keys.BUILD], target_filename)])

        try:
            subprocess.run([*compile_command, *file_to_compile], stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(errors.COMPILATION_FAILED, error=error.stderr.decode('UTF-8'))

    Logger.end('Compilation successful')

####################################################################################################

def _get_files_to_recompile(config):
    """
    Return a list of source files that, given the existing object files in the "build" folder, need
    to be (re)compiled.

    :param config: The configuration to operate on.

    :returns: A list of files to recompile.

    :raises TechnicalError: a recipe failed to be computed.
    """
    import os
    import subprocess

    from .constants             import keys
    from .errors                import errors
    from .errors.exceptions     import TechnicalError
    from .system.file_utilities import get_files

    obj_timestamp = {}

    for file in get_files(config[keys.BUILD], '.o'):
        obj_timestamp[os.path.basename(file)] = os.path.getmtime(file)

    recipes = {}
    output = ''
    preproc_command = ['g++', '-I', config[keys.INCLUDE], '-MM']

    for file in get_files(config[keys.SOURCES], '.cpp'):
        try:
            output = subprocess.run([*preproc_command, file], stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(errors.RECIPE_FAILED, error.stderr.decode('UTF-8'))

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

    :param config: The configuration to operate on.

    :raises TechnicalError: a file linking failed.
    """
    import os
    import subprocess

    from .constants             import keys
    from .errors                import errors
    from .errors.exceptions     import TechnicalError
    from .logger                import Logger
    from .system.file_utilities import get_files

    Logger.begin('Linking')

    # Step 1: compiler.
    linking_command = ['g++']

    # Step 2, 3: output executable and object files.
    linking_command.extend(['-o', os.path.join(config[keys.BINARY], config[keys.OUTPUT])])
    linking_command.extend(get_files(config[keys.BUILD], '.o'))

    # Step 4: libraries.
    if config[keys.LIBRARIES]:
        linking_command.extend('-l' + x for x in config[keys.LIBRARIES])

    try:
        subprocess.run(linking_command, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as error:
        raise TechnicalError(errors.LINKING_FAILED, error.stderr.decode('UTF-8'))

    Logger.end('Linking successful')
