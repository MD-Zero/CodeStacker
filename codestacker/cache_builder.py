#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache building utility--for compilation optimization.
"""

####################################################################################################

CACHE_FILENAME = 'codestacker_cache.yaml'

####################################################################################################

_FILES = 'FILES'
_OBJS = 'OBJECTS'

def get_files_to_compile(config):
    """
    Return a list of files to (re)compile.
    """
    import os

    from .             import keys
    from .file_handler import dump_yaml, load_yaml

    # Dereferenced for performance.
    build_dir = config[keys.BUILD]
    include_dir = config[keys.INCLUDE]
    sources_dir = config[keys.SOURCES]

    cache_file = os.path.join(build_dir, CACHE_FILENAME)
    old_cache = {}
    new_cache = {}

    if not os.path.exists(cache_file):
        new_cache = old_cache = _build_cache(include_dir, sources_dir)
    else:
        new_cache = _build_cache(include_dir, sources_dir)
        old_cache = load_yaml(cache_file)

        _check_cache(old_cache)

    dump_yaml(new_cache, cache_file)

    new_files, new_objects = new_cache[_FILES], new_cache[_OBJS]
    old_files, old_objects = old_cache[_FILES], old_cache[_OBJS]

    to_compile = set()

    # Add all new source files.
    to_compile.update(new_files.keys() - old_files.keys())

    # Add all new objects to compile.
    for object_file, source_files in new_objects.items():
        if not os.path.exists(os.path.join(build_dir, object_file)):
            to_compile.update(source_files)

    # Add all modified header and source files.
    for file, datetime in new_files.items():
        if (file in old_files) and (datetime > old_files[file]):
            if file.endswith('.cpp'):
                to_compile.add(file)
            elif file.endswith('.hpp'):
                to_compile.update(_get_impacted_sources(file, new_objects))

    to_compile = set(x for x in to_compile if x.endswith('.cpp'))

    return to_compile

####################################################################################################

_ERROR_RECIPE = 'recipe creation failed'

def _build_cache(include_dir, sources_dir):
    """
    Build a dictionary of source files, their timestamps and compilation recipe.
    """
    import os
    import subprocess

    from .exceptions  import TechnicalError
    from .file_system import get_files

    cache = {_OBJS: {}, _FILES: {}}

    try:
        for source in get_files(sources_dir, '.cpp'):
            recipe = subprocess.check_output(['g++', '-I', include_dir, '-MM', source])

            target, prerequisites = recipe.decode('UTF-8').split(':', 1)

            # Remove any backslashes from the prerequisites.
            prerequisites = prerequisites.replace('\\', '').split()

            for file in prerequisites:
                cache[_FILES].update({file: os.path.getmtime(file)})

            cache[_OBJS].update({target: prerequisites})
    except subprocess.CalledProcessError:
        raise TechnicalError(_ERROR_RECIPE)

    return cache

####################################################################################################

def _get_impacted_sources(header_file, object_files):
    """
    Return all source files whose build depends on the header in input.
    """
    to_compile = set()

    for object_file, files in object_files.items():
        if header_file in files:
            to_compile.update(x for x in files if x.endswith('.cpp'))

    return to_compile

####################################################################################################

_ERROR_CACHE_CORRUPTED = 'cache file is corrupted (hint: remove it and re-build)'

def _check_cache(cache):
    """
    Check if the cache (loaded from a file) is not corrupted.
    """
    from .exceptions import TechnicalError

    if (_FILES not in cache) or (_OBJS not in cache):
        raise TechnicalError(_ERROR_CACHE_CORRUPTED)
