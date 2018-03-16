#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Core helper functions.
"""

####################################################################################################

def get_files_to_recompile(config):
    """
    Return a list of source files that, given the existing object files in the "build" folder, need
    to be (re)compiled.

    :param config: The configuration to operate on.

    :returns: A list of files to recompile.
    """
    import os

    from codestacker.constants             import keys, extensions
    from codestacker.system.file_utilities import get_files

    # Dereferenced for performance.
    build_dir = config[keys.BUILD]
    to_compile = set()

    for target, prerequisites in _get_recipes(config[keys.SOURCES], config[keys.INCLUDE]).items():
        # Case 1: new targets.
        if target not in [os.path.basename(x) for x in get_files(build_dir, '.o')]:
            to_compile.update(prerequisites)
        # Case 2: modified source files.
        else:
            for file in prerequisites:
                if os.path.getmtime(file) > os.path.getmtime(os.path.join(build_dir, target)):
                    to_compile.add(file)

    to_compile = set(x for x in to_compile if x.endswith(extensions.SOURCES))

    return to_compile

####################################################################################################

def _get_recipes(sources_dir, include_dir):
    """
    Get a list of recipes needed to (re)compute the dependencies.

    :param sources_dir: The sources directory to look in.
    :param include_dir: The include directory to look in.

    :returns: A list of recipes.

    :raises TechnicalError: a recipe failed to compute.
    """
    import subprocess

    from codestacker.constants             import extensions
    from codestacker.errors                import errors
    from codestacker.errors.exceptions     import TechnicalError
    from codestacker.system.file_utilities import get_files

    output = ''
    preproc_command = ['g++', '-I', include_dir, '-MM']
    recipes = {}

    for file in get_files(sources_dir, extensions.SOURCES):
        try:
            output = subprocess.run([*preproc_command, file], stdout=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as error:
            raise TechnicalError(errors.RECIPE_FAILED, error=error.stderr.decode('UTF-8'))

        target, prerequisites = output.stdout.decode('UTF-8').split(':', 1)

        recipes[target] = prerequisites.replace('\\', '').split()

    return recipes
