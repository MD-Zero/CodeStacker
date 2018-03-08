#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate the configuration.
"""

####################################################################################################

def validate_config(config):
    """
    Validate the correctness of a configuration.

    :param config: The configuration to operate on.
    """
    from codestacker.logger import Logger

    Logger.begin('Checking configuration...')

    _check_keys(config)
    _check_and_substitute_vars(config)

    Logger.end('Configuration valid')

####################################################################################################

def _check_keys(config):
    """
    Perform presence and type checks on a configuration keys' values.

    :param config: The configuration to operate on.
    """
    from codestacker.constants import keys as K

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
    Perform existence and type checks on a key/value pair.

    :param key: The key to check.
    :param value: The value to check.
    :param key_type: The key's type to check.
    :param optional: An optional boolean to check... optional keys.
    """
    from codestacker.constants  import errors as E
    from codestacker.exceptions import FunctionalError

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

    from codestacker.constants   import errors as E
    from codestacker.exceptions  import GraphError, TechnicalError, FunctionalError
    from codestacker.graph_tools import is_directed_acyclic_graph, get_topological_ordering

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
