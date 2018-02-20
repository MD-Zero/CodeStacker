#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML configuration file inspector.
"""

####################################################################################################

def select_config(configs, config_name):
    """
    From the configurations in input, extract the wished one.
    """
    from .exceptions import TechnicalError
    from .logger     import log_info

    for config in configs:
        if config_name in config:
            log_info('Found "{}" configuration'.format(config_name))

            return config[config_name]

    raise TechnicalError('configuration "{}" not found'.format(config_name))

####################################################################################################

def validate_config(config):
    """
    Validate the correctness of the configuration in input.
    """
    from .logger import log_info, log_ok

    log_info('>> Validating configuration...')

    _check_keys(config)
    _check_and_substitute_vars(config)

    log_ok('<< Success')

####################################################################################################

def adapt_config(root, config):
    """
    Transform all "path" in configuration keys into their absolute equivalent.
    """
    from .            import constants
    from .file_system import get_absolute_path

    config[constants.KEY_DIR_BIN] = get_absolute_path(root, config[constants.KEY_DIR_BIN])
    config[constants.KEY_DIR_BUILD] = get_absolute_path(root, config[constants.KEY_DIR_BUILD])
    config[constants.KEY_DIR_INCLUDE] = get_absolute_path(root, config[constants.KEY_DIR_INCLUDE])
    config[constants.KEY_DIR_SOURCE] = get_absolute_path(root, config[constants.KEY_DIR_SOURCE])

####################################################################################################

def _check_keys(config):
    """
    Perform presence and type checks for the configuration keys.
    """
    from . import constants as keys

    _check_key(config, keys.KEY_DIR_BIN, str)
    _check_key(config, keys.KEY_DIR_BUILD, str)
    _check_key(config, keys.KEY_DIR_INCLUDE, str)
    _check_key(config, keys.KEY_DIR_SOURCE, str)
    _check_key(config, keys.KEY_OUTPUT, str)

    _check_key(config, keys.KEY_COMPILER_OPTIONS, list, True)
    _check_key(config, keys.KEY_LIBRARIES, list, True)

####################################################################################################

def _check_key(config, key, key_type, optional=False):
    """
    Perform presence and type checks for mandatory and optional configuration keys.
    """
    from .exceptions import TechnicalError

    if (key in config) and (not isinstance(config[key], key_type)):
        raise TechnicalError(
            'key "{}" is of incorrect type (should be "{}")'.format(key, key_type.__name__))
    elif (not optional) and (key not in config):
        raise TechnicalError('missing mandatory "{}" key'.format(key))

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
        raise TechnicalError(_ERROR_VAR_GRAPH.format(error.get_message()))

    # Based on their topological ordering, proceed with the substitutions.
    for var in get_topological_ordering(all_vars):
        for key, value in config.items():
            if not isinstance(value, str):
                continue

            config[key] = config[key].replace('${{{}}}'.format(var), config[var])
