#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adapt the configuration.
"""

####################################################################################################

def adapt_config(config):
    """
    Adapt configuration keys to match process requirements (values, definition, etc.).
    """
    from codestacker        import keys as K
    from codestacker.logger import Logger

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
    Check if directory for the given exist:
        - raise an error if absent and mandatory;
        - create it if optional.
    """
    import os

    from codestacker            import errors as E
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
    Turn the configuration key's values into a set.
    """
    if key in config:
        config[key] = set(config[key])
    else:
        config[key] = set()
