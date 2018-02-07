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
    from .helpers import die
    from .logger  import log_info

    for config in configs:
        if config_name in config:
            log_info('Found "{}" configuration'.format(config_name))

            return config[config_name]

    die('Configuration "{}" not found'.format(config_name))

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

_ERROR_MISSING_KEY = 'Missing mandatory "{}" key'
_ERROR_WRONG_TYPE = 'Key "{}" is of incorrect type (should be "{}")'

def _check_keys(config):
    """
    Perform presence and type checks for the configuration keys.
    """
    from .        import constants as keys
    from .helpers import die

    # "output" (mandatory).
    if keys.KEY_OUTPUT not in config:
        die(_ERROR_MISSING_KEY.format(keys.KEY_OUTPUT))
    elif not isinstance(config[keys.KEY_OUTPUT], str):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_OUTPUT, 'string'))

    # "dir_include" (mandatory).
    if keys.KEY_DIR_INCLUDE not in config:
        die(_ERROR_MISSING_KEY.format(keys.KEY_DIR_INCLUDE))
    elif not isinstance(config[keys.KEY_DIR_INCLUDE], str):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_DIR_INCLUDE, 'string'))

    # "dir_source" (mandatory).
    if keys.KEY_DIR_SOURCE not in config:
        die(_ERROR_MISSING_KEY.format(keys.KEY_DIR_SOURCE))
    elif not isinstance(config[keys.KEY_DIR_SOURCE], str):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_DIR_SOURCE, 'string'))

    # "dir_bin" (optional).
    if (keys.KEY_DIR_BIN in config) and\
       (not isinstance(config[keys.KEY_DIR_BIN], str)):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_DIR_BIN, 'string'))

    # "dir_build" (optional).
    if (keys.KEY_DIR_BUILD in config) and\
       (not isinstance(config[keys.KEY_DIR_BUILD], str)):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_DIR_BUILD, 'string'))

    # "compiler_options" (optional).
    if (keys.KEY_COMPILER_OPTIONS in config) and\
       (not isinstance(config[keys.KEY_COMPILER_OPTIONS], list)):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_COMPILER_OPTIONS, 'list'))

    # "libraries" (optional).
    if (keys.KEY_LIBRARIES in config) and\
       (not isinstance(config[keys.KEY_LIBRARIES], list)):
        die(_ERROR_WRONG_TYPE.format(keys.KEY_LIBRARIES, 'list'))

####################################################################################################

_REGEX_VAR = r'\${(\w+)}'

def _check_and_substitute_vars(config):
    """
    Check if variables are well-defined (type + existence), and if there are no cyclic references.
    Once done, proceed with the substitution.
    """
    import re

    from .graph_tools import is_directed_acyclic_graph, get_topological_ordering
    from .helpers     import die

    # Check first variables correctness.
    for value in config.values():
        if not isinstance(value, str):
            continue

        for var in re.findall(_REGEX_VAR, value):
            if var not in config:
                die('Variable "{}" is undefined'.format(var))
            elif not isinstance(config[var], str):
                die('Variable "{}" is not of type "string"'.format(var))

    # Gather all variables in one place.
    all_vars = {}

    for key, value in config.items():
        if not isinstance(value, str):
            continue

        all_vars[key] = set(re.findall(_REGEX_VAR, value))

    # Check if variables form a DAG (Directed Acyclic Graph).
    if not is_directed_acyclic_graph(all_vars):
        die('Cyclic variable reference detected')

    # Based on their topological ordering, proceed with the substitutions.
    ordered_vars = get_topological_ordering(all_vars)

    for var in ordered_vars:
        for key, value in config.items():
            if not isinstance(value, str):
                continue

            config[key] = config[key].replace('${{{}}}'.format(var), config[var])
