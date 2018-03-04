#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML configuration file inspector.
"""

####################################################################################################

def get_config(arguments) -> dict:
    """
    From the arguments in input, load the YAML configuration file, extract the wished configuration
    and return it.
    """
    import os

    from .             import errors as E
    from .             import keys as K
    from .exceptions   import TechnicalError
    from .file_handler import load_yaml

    config = load_yaml(arguments['file']).get(arguments['config'])

    if config is None:
        raise TechnicalError(E.CONFIG_NOT_FOUND.format(arguments['config']))

    # Add those special keys to the configuration, for later processing.
    config[K.ROOT] = os.path.realpath(os.path.dirname(arguments['file']))
    config[K.COMMAND] = arguments['command']

    return config

####################################################################################################

def validate_config(config):
    """
    Validate the correctness of the configuration in input.
    """
    from .logger import Logger

    Logger.begin('Checking configuration...')

    _check_keys(config)
    _check_and_substitute_vars(config)

    Logger.end('Configuration valid')

####################################################################################################

def adapt_config(config):
    """
    Adapt configuration keys to match process requirements (values, definition, etc.).
    """
    from .       import keys as K
    from .logger import Logger

    # Dereferenced for performance.
    root = config[K.ROOT]

    Logger.begin('Adapting configuration keys...')

    _adapt_path(root, config, K.INCLUDE)
    _adapt_path(root, config, K.SOURCES)

    _adapt_path(root, config, K.BINARY, True)
    _adapt_path(root, config, K.BUILD, True)

    _turn_into_set(config, K.FLAGS)
    _turn_into_set(config, K.LIBRARIES)

    Logger.end('Done')

####################################################################################################

def run_config(config):
    """
    Run the wished configuration.
    """
    from .        import keys as K
    from .builder import build
    from .cleaner import clean

    # Dereferenced for performance.
    command = config[K.COMMAND]

    if command == 'build':
        build(config)
    elif command == 'clean':
        clean(config)

####################################################################################################

def _check_keys(config):
    """
    Perform presence and type checks for the configuration keys' values.
    """
    from . import keys as K

    # Mandatory attributes.
    _check_key(K.BINARY, config.get(K.BINARY), str)
    _check_key(K.BUILD, config.get(K.BUILD), str)
    _check_key(K.INCLUDE, config.get(K.INCLUDE), str)
    _check_key(K.OUTPUT, config.get(K.OUTPUT), str)
    _check_key(K.SOURCES, config.get(K.SOURCES), str)

    # Optional attributes.
    _check_key(K.FLAGS, config.get(K.FLAGS), list, True)
    _check_key(K.LIBRARIES, config.get(K.LIBRARIES), list, True)

####################################################################################################

def _check_key(key, value, key_type, optional=False):
    """
    Perform presence and type checks for mandatory and optional configuration keys.
    """
    from .           import errors as E
    from .exceptions import FunctionalError

    if (value is None) and (not optional):
        raise FunctionalError(E.MISSING_KEY.format(key))
    elif (value is not None) and (not isinstance(value, key_type)):
        raise FunctionalError(E.INCORRECT_KEY_TYPE.format(key, key_type.__name__))

####################################################################################################

_REGEX_VAR = r'\$(\w+)'

def _check_and_substitute_vars(config):
    """
    Check if variables are well-defined (type + existence), and if there are no cyclic references.
    Once done, proceed with the substitution.
    """
    import re

    from .            import errors as E
    from .exceptions  import GraphError, TechnicalError, FunctionalError
    from .graph_tools import is_directed_acyclic_graph, get_topological_ordering

    # Check first variables correctness.
    for value in config.values():
        if not isinstance(value, str):
            continue

        for var in re.findall(_REGEX_VAR, value):
            if var not in config:
                raise FunctionalError(E.UNDEFINED_VAR.format(var))
            elif not isinstance(config[var], str):
                raise FunctionalError(E.WRONG_VAR_TYPE.format(var))

    # Gather all variables in one place.
    all_vars = {}

    for key, value in config.items():
        if not isinstance(value, str):
            continue

        all_vars[key] = set(re.findall(_REGEX_VAR, value))

    # Check if variables form a DAG (Directed Acyclic Graph).
    try:
        is_directed_acyclic_graph(all_vars)
    except GraphError as error:
        raise TechnicalError(E.ERROR_VAR_GRAPH.format(error.message))

    # Based on their topological ordering, proceed with the substitutions.
    for var in get_topological_ordering(all_vars):
        for key, value in config.items():
            if not isinstance(value, str):
                continue

            config[key] = config[key].replace('${}'.format(var), config[var])

####################################################################################################

def _adapt_path(root, config, key, should_create=False):
    """
    Check if directory for the given exist:
        - raise an error if absent and mandatory;
        - create it if optional.
    """
    import os

    from .           import errors as E
    from .exceptions import TechnicalError
    from .logger     import Logger

    abs_path = os.path.join(root, config[key])

    if not os.path.exists(abs_path):
        if not should_create:
            raise TechnicalError(E.FOLDER_NOT_FOUND.format(abs_path))
        else:
            Logger.warning('Folder "{}" not found: creating it...'.format(abs_path))

            os.makedirs(abs_path)

    config[key] = abs_path

####################################################################################################

def _turn_into_set(config, key):
    """
    Turn the configuration key's values into a set.
    """
    if key in config:
        config[key] = set(config[key])
    else:
        config[key] = set()
