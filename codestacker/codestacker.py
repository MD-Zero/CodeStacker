#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main script logic.
"""

####################################################################################################

def main():
    """
    Script's main function.
    """
    import sys
    import traceback

    from .args_parser                import parse_args
    from .config_inspector.adaptor   import adapt_config
    from .config_inspector.retriever import get_config
    from .config_inspector.validator import validate_config
    from .constants                  import keys
    from .core.builder               import build
    from .core.cleaner               import clean
    from .errors.exceptions          import Error
    from .logger                     import Logger

    arguments = parse_args()

    try:
        config = get_config(arguments)

        validate_config(config)
        adapt_config(config)

        command = config[keys.COMMAND]
        verbose = config[keys.VERBOSE]

        if command == 'build':
            build(config, verbose)
        elif command == 'clean':
            clean(config)
    except Error as error:
        error.print()
        Logger.abort('Aborting')
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        Logger.abort('Keyboard interruption')
        sys.exit(1)
    except BaseException:
        traceback.print_exc()
        sys.exit(1)
    else:
        Logger.close('End of script')
        sys.exit(0)
