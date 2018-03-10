#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adapt the configuration.
"""

####################################################################################################

def adapt_config(config):
    """
    Adapt a configuration to match process requirements (values, definition, etc.).

    :param config: The configuration to adapt.
    """
    from codestacker.constants import keys
    from codestacker.logger    import Logger

    # Dereferenced for performance.
    root = config[keys.ROOT]

    Logger.begin('Adapting configuration keys...')

    _adapt_path(root, config, keys.INCLUDE)
    _adapt_path(root, config, keys.SOURCES)

    _adapt_path(root, config, keys.BINARY, True)
    _adapt_path(root, config, keys.BUILD, True)

    _turn_into_set(config, keys.FLAGS)
    _turn_into_set(config, keys.LIBRARIES)

    Logger.end('Done')

####################################################################################################

def _adapt_path(root, config, key, should_create=False):
    """
    Turn a directory path into its absolute equivalent.

    :param root: The root directory to refer from.
    :param config: The configuration to look in.
    :param key: The configuration key to adapt.
    :param should_create: An optional boolean about whether a non-existent directory should be
                          created or not.

    :raises TechnicalError: the directory is non-existent (and should be).
    """
    import os

    from codestacker.errors            import errors
    from codestacker.errors.exceptions import TechnicalError
    from codestacker.logger            import Logger

    abs_path = os.path.join(root, config[key])

    if not os.path.exists(abs_path):
        if not should_create:
            raise TechnicalError(errors.FOLDER_NOT_FOUND, abs_path)
        else:
            Logger.warning('Folder "{}" not found: creating it...'.format(abs_path))

            os.makedirs(abs_path)

    config[key] = abs_path

####################################################################################################

def _turn_into_set(config, key):
    """
    Turn a configuration key's value into a set.

    :param config: The configuration to operate on.
    :param key: The key to transform.
    """
    if key in config:
        config[key] = set(config[key])
    else:
        config[key] = set()
