#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compilation + linking.
"""

####################################################################################################

def build(config, verbose):
    """
    Build the project (compile + link).

    :param config: The configuration to operate on.
    """
    from codestacker.logger import Logger

    Logger.begin('Building...')

    _validate_sources(config)

    _compile(config, verbose)
    _link(config, verbose)

    Logger.end('Done')

####################################################################################################

def _validate_sources(config):
    """
    Check if headers and sources filenames are valid.

    :param config: The configuration to operate on.
    """
    from codestacker.constants             import keys, extensions
    from codestacker.logger                import Logger
    from codestacker.system.file_utilities import check_files

    Logger.info('Check headers and sources')

    check_files(config[keys.INCLUDE], extensions.HEADERS)
    check_files(config[keys.SOURCES], extensions.SOURCES)

####################################################################################################

_SPECIAL_FLAG = '-fdiagnostics-color=always'

def _compile(config, verbose):
    """
    Compile the source files into object files.

    :param config: The configuration to operate on.
    :param verbose: The boolean flag to output compilation command.

    :raises TechnicalError: a source file compilation failed.
    """
    import os
    import re
    import subprocess

    from .helpers                      import get_files_to_recompile
    from codestacker.constants         import keys, extensions
    from codestacker.errors            import errors
    from codestacker.errors.exceptions import TechnicalError
    from codestacker.logger            import Logger

    files_to_compile = get_files_to_recompile(config)

    if not files_to_compile:
        Logger.info('Nothing to (re)compile')
        return

    Logger.begin('Compilation...')

    # Step 1: compiler.
    compile_command = ['g++']

    # Step 2: compilation flags.
    compile_command.extend(config[keys.FLAGS])

    # Add this special flag to force the compiler to print its output in colors.
    if _SPECIAL_FLAG not in compile_command:
        compile_command.append(_SPECIAL_FLAG)

    # Step 3: include directory.
    compile_command.extend(['-I', config[keys.INCLUDE]])

    pattern = re.compile(r'(' + r'|'.join([re.escape(x) for x in extensions.SOURCES]) + r')$')

    for file in files_to_compile:
        Logger.info('Compiling {}'.format(os.path.relpath(file, config[keys.ROOT])))

        # Step 4: source file to compile.
        file_to_compile = ['-c', file]

        target_filename = pattern.sub('.o', os.path.basename(file))

        # Step 5: object file to produce.
        file_to_compile.extend(['-o', os.path.join(config[keys.BUILD], target_filename)])

        full_command = [*compile_command, *file_to_compile]

        try:
            if verbose:
                Logger.info('Execute:\n{}'.format(' '.join(full_command)))

            subprocess.run(full_command, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(errors.COMPILATION_FAILED, error=error.stderr.decode('UTF-8'))

    Logger.end('Success')

####################################################################################################

def _link(config, verbose):
    """
    Link the object files into an executable.

    :param config: The configuration to operate on.
    :param verbose: The boolean flag to output linking command.

    :raises TechnicalError: the linking command failed.
    """
    import os
    import subprocess

    from codestacker.constants             import keys
    from codestacker.errors                import errors
    from codestacker.errors.exceptions     import TechnicalError
    from codestacker.logger                import Logger
    from codestacker.system.file_utilities import get_files

    Logger.begin('Linking...')

    # Step 1: compiler.
    linking_command = ['g++']

    # Step 2, 3: output executable and object files.
    linking_command.extend(['-o', os.path.join(config[keys.BINARY], config[keys.OUTPUT])])
    linking_command.extend(get_files(config[keys.BUILD], '.o'))

    # Step 4: libraries.
    if config[keys.LIBRARIES]:
        linking_command.extend('-l' + library for library in config[keys.LIBRARIES])

    try:
        if verbose:
            Logger.info('Execute:\n{}'.format(' '.join(linking_command)))

        subprocess.run(linking_command, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as error:
        raise TechnicalError(errors.LINKING_FAILED, error=error.stderr.decode('UTF-8'))

    Logger.end('Success')
