#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML configuration file validator.
"""

REGEX_VAR = r'\${(\w+)}'

####################################################################################################

def validate(config):
    """
    Validate the correctness of a configuration file.
    """
    if isinstance(config, dict):
        config = [config]

    for profile in config:
        check_required_keys(profile)
        # check_keys_type(profile)
        check_vars(profile)
        substitute_vars(profile)

####################################################################################################

ERROR_MANDATORY = 'Missing mandatory key in profile "{}": "{}".'
ERROR_PROFILE = 'Missing mandatory "profile" key.'

def check_required_keys(profile):
    """
    Perform different checks regarding the profile's keys.
    """
    from .constants import Keys
    from .helpers   import print_and_die

    if Keys.PROFILE not in profile:
        print_and_die(ERROR_PROFILE)

    profile_name = profile[Keys.PROFILE]

    if Keys.DIR_INCLUDE not in profile:
        print_and_die(ERROR_MANDATORY.format(profile_name, Keys.DIR_INCLUDE))

    if Keys.DIR_SOURCE not in profile:
        print_and_die(ERROR_MANDATORY.format(profile_name, Keys.DIR_SOURCE))

    if Keys.OUTPUT not in profile:
        print_and_die(ERROR_MANDATORY.format(profile_name, Keys.OUTPUT))

####################################################################################################

def check_keys_type():
    """
    Check the type-correctness of configuration keys.
    """
    pass

####################################################################################################

ERROR_CYCLE = 'Profile "{}" has cyclic variable reference(s): please fix it.'
ERROR_MISSING_VAR = 'Variable "{}" in profile "{}" is undefined.'
ERROR_WRONG_TYPE = 'Variable "{}" is not of type "string".'

def check_vars(profile):
    """
    Check if referenced variables are well-defined (type "string" + existence), and if there are no
    cyclic references.
    """
    import re

    from .constants   import Keys
    from .graph_tools import is_directed_acyclic_graph
    from .helpers     import print_and_die

    profile_name = profile[Keys.PROFILE]

    for value in profile.values():
        if not isinstance(value, str):
            continue

        for var in re.findall(REGEX_VAR, value):
            # Case where the variable doesn't exist in the profile.
            if var not in profile:
                print_and_die(ERROR_MISSING_VAR.format(var, profile_name))

            # Case where the variable's type is not "string".
            if not isinstance(profile[var], str):
                print_and_die(ERROR_WRONG_TYPE.format(var))

    if not is_directed_acyclic_graph(get_all_vars(profile)):
        print_and_die(ERROR_CYCLE.format(profile_name))

####################################################################################################

def substitute_vars(profile):
    """
    Parse the given profile and substitute variables with real values.
    """
    from .graph_tools import get_topological_ordering

    ordered_vars = get_topological_ordering(get_all_vars(profile))

    # Based on their topological ordering, proceed with the substitutions.
    for var in ordered_vars:
        for key, value in profile.items():
            if not isinstance(value, str):
                continue

            profile[key] = profile[key].replace('${{{}}}'.format(var), profile[var])

####################################################################################################

def get_all_vars(profile):
    """
    Helper function to retrieve all profile's variables in one place.
    """
    import re

    all_vars = {}

    for key, value in profile.items():
        if not isinstance(value, str):
            continue

        # The existence of variable is checked first because we don't want keys with empty values.
        if re.search(REGEX_VAR, value):
            all_vars[key] = set(re.findall(REGEX_VAR, value))

    return all_vars
