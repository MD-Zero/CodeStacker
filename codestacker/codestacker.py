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

    from .args_parser      import parse_args
    from .config_inspector import get_config, validate_config, adapt_config, run_config
    from .exceptions       import Error
    from .logger           import log_ko

    arguments = parse_args()

    try:
        config = get_config(arguments)

        validate_config(config)
        adapt_config(config)
        run_config(config)
    except Error as error:
        error.print()
    except KeyboardInterrupt:
        print()
        log_ko('Keyboard interruption: stopping')
    except BaseException:
        traceback.print_exc()
