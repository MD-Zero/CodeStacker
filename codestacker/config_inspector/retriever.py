#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Retrieve a configuration.
"""

####################################################################################################

def get_config(arguments):
    """
    Extract the wished configuration, based on the arguments in input.

    :param arguments: The arguments passed to CodeStacker (through CLI).

    :returns: A configuration extracted from a YAML file (retrieved from arguments).

    :raises TechnicalError: the configuration name is missing from the YAML file.
    """
    import os

    from codestacker.constants           import keys
    from codestacker.errors              import errors
    from codestacker.errors.exceptions   import TechnicalError
    from codestacker.system.yaml_handler import load_yaml

    config = load_yaml(arguments['file']).get(arguments['config'])

    if config is None:
        raise TechnicalError(errors.CONFIG_NOT_FOUND, arguments['config'])

    # Add those special keys to the configuration, for later processing.
    config[keys.COMMAND] = arguments['command']
    config[keys.ROOT] = os.path.realpath(os.path.dirname(arguments['file']))

    return config
