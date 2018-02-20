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
    import os
    import traceback

    from .args_parser      import parse_args
    from .builder          import build
    from .cleaner          import clean
    from .config_inspector import select_config, validate_config, adapt_config
    from .exceptions       import Error
    from .file_loader      import load_yaml
    from .logger           import log_ko

    arguments = parse_args()

    filename = arguments['file']
    root = os.path.dirname(os.path.realpath(filename))

    try:
        config = select_config(load_yaml(filename), arguments['config'])

        validate_config(config)
        adapt_config(root, config)

        command = arguments['command']

        if command == 'build':
            build(root, config)
        elif command == 'clean':
            clean(root, config)
    except Error as error:
        error.print()
    except KeyboardInterrupt:
        print()
        log_ko('Keyboard interruption: stopping')
    except BaseException:
        traceback.print_exc()
