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
    from codestacker.constants import keys

    # Mandatory attributes.
    _check_key(keys.BINARY, config.get(keys.BINARY), str)
    _check_key(keys.BUILD, config.get(keys.BUILD), str)
    _check_key(keys.INCLUDE, config.get(keys.INCLUDE), str)
    _check_key(keys.OUTPUT, config.get(keys.OUTPUT), str)
    _check_key(keys.SOURCES, config.get(keys.SOURCES), str)

    # Optional attributes.
    _check_key(keys.FLAGS, config.get(keys.FLAGS), list, True)
    _check_key(keys.LIBRARIES, config.get(keys.LIBRARIES), list, True)

####################################################################################################

def _check_key(key, value, key_type, optional=False):
    """
    Perform existence and type checks on a key/value pair.

    :param key: The key to check.
    :param value: The value to check.
    :param key_type: The key's type to check.
    :param optional: An optional boolean to check... optional keys.

    :raises FunctionalError: one mandatory key is missing or of wrong type.
    """
    from codestacker.errors            import errors
    from codestacker.errors.exceptions import FunctionalError

    if (value is None) and (not optional):
        raise FunctionalError(errors.MISSING_KEY, key)
    elif (value is not None) and (not isinstance(value, key_type)):
        raise FunctionalError(errors.WRONG_KEY_TYPE, key)

####################################################################################################

_REGEX_VAR = r'\$(\w+)'

def _check_and_substitute_vars(config):
    """
    Check if variables are well-defined (type + existence), and proceed with variables substitution.

    :param config: The configuration to operate on.

    :raises FunctionalError: a variable is undefined or of wrong type.
    :raises TechnicalError: one or many cyclic references were detected among variables.
    """
    import re

    from codestacker.errors            import errors
    from codestacker.errors.exceptions import GraphError, TechnicalError, FunctionalError
    from codestacker.graph_tools       import is_directed_acyclic_graph, get_topological_ordering

    # Check first variables correctness.
    for value in config.values():
        if not isinstance(value, str):
            continue

        for var in re.findall(_REGEX_VAR, value):
            if var not in config:
                raise FunctionalError(errors.UNDEFINED_VAR, var)
            elif not isinstance(config[var], str):
                raise FunctionalError(errors.WRONG_VAR_TYPE, var)

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
        raise TechnicalError(errors.ERROR_VAR_GRAPH, error.args[0])

    # Based on their topological ordering, proceed with the substitutions.
    for var in get_topological_ordering(all_vars):
        for key, value in config.items():
            if not isinstance(value, str):
                continue

            config[key] = config[key].replace('${}'.format(var), config[var])
