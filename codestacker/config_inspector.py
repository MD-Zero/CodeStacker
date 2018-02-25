#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML configuration file inspector.
"""

####################################################################################################

_ERROR_NO_CONFIG = 'configuration "{}" not found'

def get_config(arguments):
    """
    From the arguments in input, load the YAML configuration file, extract the wished configuration
    and return it.
    """
    import os

    from .             import keys
    from .exceptions   import TechnicalError
    from .file_handler import load_yaml

    config = load_yaml(arguments['file']).get(arguments['config'])

    if config is None:
        raise TechnicalError(_ERROR_NO_CONFIG.format(arguments['config']))

    # Add those special keys to the configuration, for later processing.
    config[keys.ROOT] = os.path.realpath(os.path.dirname(arguments['file']))
    config[keys.COMMAND] = arguments['command']

    return config

####################################################################################################

def validate_config(config):
    """
    Validate the correctness of the configuration in input.
    """
    from .logger import Logger

    Logger.log_begin('Checking configuration...')

    _check_keys_values(config)
    _check_and_substitute_vars(config)

    Logger.log_end('Configuration valid')

####################################################################################################

def adapt_config(config):
    """
    Transform all "path" in configuration keys into their absolute equivalent.
    """
    from .            import keys
    from .file_system import get_absolute_path
    from .logger      import Logger

    # Dereferenced for performance.
    root = config[keys.ROOT]

    Logger.log_begin('Adapting configuration paths...')

    config[keys.BINARY] = get_absolute_path(root, config[keys.BINARY])
    config[keys.BUILD] = get_absolute_path(root, config[keys.BUILD])
    config[keys.INCLUDE] = get_absolute_path(root, config[keys.INCLUDE])
    config[keys.SOURCES] = get_absolute_path(root, config[keys.SOURCES])

    Logger.log_end('Done')

####################################################################################################

def run_config(config):
    """
    Run the wished configuration.
    """
    from .        import keys
    from .builder import build
    from .cleaner import clean

    command = config[keys.COMMAND]

    if command == 'build':
        build(config)
    elif command == 'clean':
        clean(config)

####################################################################################################

def _check_keys_values(config):
    """
    Perform presence and type checks for the configuration keys' values.
    """
    from . import keys

    # Mandatory attributes.
    _check_key_value(config, keys.BINARY, str)
    _check_key_value(config, keys.BUILD, str)
    _check_key_value(config, keys.INCLUDE, str)
    _check_key_value(config, keys.SOURCES, str)
    _check_key_value(config, keys.OUTPUT, str)

    # Optional attributes.
    _check_key_value(config, keys.FLAGS, list, True)
    _check_key_value(config, keys.LIBRARIES, list, True)

####################################################################################################

_ERROR_KEY_INCORRECT = 'key "{}" is of incorrect type (should be "{}")'
_ERROR_KEY_MISSING = 'missing mandatory "{}" key'

def _check_key_value(config, key, key_type, optional=False):
    """
    Perform presence and type checks for mandatory and optional configuration keys.
    """
    from .exceptions import FunctionalError

    value = config.get(key)

    if (value is None) and (not optional):
        raise FunctionalError(_ERROR_KEY_MISSING.format(value))
    elif (value is not None) and (not isinstance(value, key_type)):
        raise FunctionalError(_ERROR_KEY_INCORRECT.format(key, key_type.__name__))

####################################################################################################

_REGEX_VAR = r'\${(\w+)}'

_ERROR_VAR_UNDEFINED = 'variable "{}" is undefined'
_ERROR_VAR_TYPE = 'variable "{}" is not of type "str"'
_ERROR_VAR_GRAPH = 'error in variables references ({})'

def _check_and_substitute_vars(config):
    """
    Check if variables are well-defined (type + existence), and if there are no cyclic references.
    Once done, proceed with the substitution.
    """
    import re

    from .exceptions  import GraphError, TechnicalError, FunctionalError
    from .graph_tools import is_directed_acyclic_graph, get_topological_ordering

    # Check first variables correctness.
    for value in config.values():
        if not isinstance(value, str):
            continue

        for var in re.findall(_REGEX_VAR, value):
            if var not in config:
                raise FunctionalError(_ERROR_VAR_UNDEFINED.format(var))
            elif not isinstance(config[var], str):
                raise FunctionalError(_ERROR_VAR_TYPE.format(var))

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
        raise TechnicalError(_ERROR_VAR_GRAPH.format(error.message))

    # Based on their topological ordering, proceed with the substitutions.
    for var in get_topological_ordering(all_vars):
        for key, value in config.items():
            if not isinstance(value, str):
                continue

            config[key] = config[key].replace('${{{}}}'.format(var), config[var])
