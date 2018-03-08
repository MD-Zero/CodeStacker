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
    from codestacker.constants import keys as K
    from codestacker.logger    import Logger

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

    from codestacker.constants  import errors as E
    from codestacker.exceptions import TechnicalError
    from codestacker.logger     import Logger

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
    Turn a configuration key's value into a set.

    :param config: The configuration to operate on.
    :param key: The key to transform.
    """
    if key in config:
        config[key] = set(config[key])
    else:
        config[key] = set()
