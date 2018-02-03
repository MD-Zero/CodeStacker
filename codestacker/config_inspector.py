#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML configuration file inspector.
"""

_REGEX_VAR = r'\${(\w+)}'

####################################################################################################

def select_config(configs, config_name):
    """
    From the configurations in input, extract the wished one.
    """
    from .helpers import print_and_die

    for config in configs:
        if config_name in config:
            return config[config_name]

    print_and_die('Configuration "{}" not found'.format(config_name))

####################################################################################################

def validate_config(config):
    """
    Validate the correctness of the configuration in input.
    """
    _check_required_keys(config)
    _check_keys_type(config)
    _check_vars(config)
    _substitute_vars(config)

####################################################################################################

_ERROR_CONFIG = 'Missing mandatory "{}" key'

def _check_required_keys(config):
    """
    Perform different checks regarding the configuration keys.
    """
    from .        import constants as keys
    from .helpers import print_and_die

    if keys.KEY_OUTPUT not in config:
        print_and_die(_ERROR_CONFIG.format(keys.KEY_OUTPUT))

    if keys.KEY_DIR_INCLUDE not in config:
        print_and_die(_ERROR_CONFIG.format(keys.KEY_DIR_INCLUDE))

    if keys.KEY_DIR_SOURCE not in config:
        print_and_die(_ERROR_CONFIG.format(keys.KEY_DIR_SOURCE))

####################################################################################################

_ERROR_WRONG_TYPE = 'Key "{}" is of incorrect type'

def _check_keys_type(config):
    """
    Check the type-correctness of configuration keys.
    """
    from .        import constants as keys
    from .helpers import print_and_die

    if not isinstance(config[keys.KEY_COMPILER_OPTIONS], (str, list)):
        print_and_die(_ERROR_WRONG_TYPE.format(keys.KEY_COMPILER_OPTIONS))

    # TODO (more to add)

####################################################################################################

def _check_vars(config):
    """
    Check if referenced variables are well-defined (type "string" + existence), and if there are no
    cyclic references.
    """
    import re

    from .            import constants as keys
    from .graph_tools import is_directed_acyclic_graph
    from .helpers     import print_and_die

    for value in config.values():
        if not isinstance(value, str):
            continue

        for var in re.findall(_REGEX_VAR, value):
            # Case where the variable doesn't exist in the configuration.
            if var not in config:
                print_and_die('Variable "{}" is undefined'.format(var))

            # Case where the variable's type is not "string".
            if not isinstance(config[var], str):
                print_and_die('Variable "{}" is not of type "string"'.format(var))

    if not is_directed_acyclic_graph(_get_all_vars(config)):
        print_and_die('Cyclic variable reference(s) detected')

####################################################################################################

def _substitute_vars(config):
    """
    Parse the given configuration and substitute variables with real values.
    """
    from .graph_tools import get_topological_ordering

    ordered_vars = get_topological_ordering(_get_all_vars(config))

    # Based on their topological ordering, proceed with the substitutions.
    for var in ordered_vars:
        for key, value in config.items():
            if not isinstance(value, str):
                continue

            config[key] = config[key].replace('${{{}}}'.format(var), config[var])

####################################################################################################

def _get_all_vars(config):
    """
    Helper function to retrieve all configuration's variables in one place.
    """
    import re

    all_vars = {}

    for key, value in config.items():
        if not isinstance(value, str):
            continue

        # The existence of variable is checked first because we don't want keys with empty values.
        if re.search(_REGEX_VAR, value):
            all_vars[key] = set(re.findall(_REGEX_VAR, value))

    return all_vars
