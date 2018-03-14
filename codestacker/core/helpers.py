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

    :raises TechnicalError: a recipe failed to be computed.
    """
    import os

    from codestacker.constants             import keys, extensions
    from codestacker.system.file_utilities import get_files

    obj_timestamp = {}

    for file in get_files(config[keys.BUILD], '.o'):
        obj_timestamp[os.path.basename(file)] = os.path.getmtime(file)

    to_compile = set()

    for obj, file_timestamp in _get_recipes(config[keys.SOURCES], config[keys.INCLUDE]).items():
        # Case 1: new targets.
        if obj not in obj_timestamp:
            to_compile.update(file_timestamp.keys())
        # Case 2: modified source files.
        else:
            for file, timestamp in file_timestamp.items():
                if timestamp > obj_timestamp[obj]:
                    to_compile.add(file)

    to_compile = set(file for file in to_compile if file.endswith(extensions.SOURCES))

    return to_compile

####################################################################################################

def _get_recipes(sources_dir, include_dir):
    """
    Get all recipes needed to (re)compute the dependencies.

    :param sources_dir: The sources directory to look in.
    :param include_dir: The include directory to look in.

    :returns: A list of recipes, each target being associated with {filename: time stamp}.

    :raises TechnicalError: a recipe failed to compute.
    """
    import os
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
            raise TechnicalError(errors.RECIPE_FAILED, error.stderr.decode('UTF-8'))

        target, prerequisites = output.stdout.decode('UTF-8').split(':', 1)

        prerequisites = prerequisites.replace('\\', '').split()

        recipes[target] = {source: os.path.getmtime(source) for source in prerequisites}

    return recipes
