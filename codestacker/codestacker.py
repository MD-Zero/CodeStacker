#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program flow:
    1. Parse the arguments.
    2. Load the YAML blueprint file content, and choose a configuration.
    3. Validate its inner structure.
    4. Adapt it: set absolute paths in keys.
    5. Run the wished configuration.
    6. Quit the program.
"""

####################################################################################################

def main():
    """
    Script's main function.
    """
    import traceback

    from .args_parser                import parse_args
    from .builder                    import build
    from .cleaner                    import clean
    from .config_inspector.adaptor   import adapt_config
    from .config_inspector.retriever import get_config
    from .config_inspector.validator import validate_config
    from .errors.exceptions          import Error
    from .logger                     import Logger

    arguments = parse_args()

    try:
        config = get_config(arguments)

        validate_config(config)
        adapt_config(config)

        command = config['_command']

        if command == 'build':
            build(config)
        elif command == 'clean':
            clean(config)
    except Error as error:
        error.print()
        Logger.abort('Aborting')
    except KeyboardInterrupt:
        print()
        Logger.error('Keyboard interruption: stopping')
    except BaseException:
        traceback.print_exc()
    else:
        Logger.close('End of script')
