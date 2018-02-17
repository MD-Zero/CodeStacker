#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script's main entry point.
"""

if __name__ == '__main__':
    import sys
    import traceback

    from .            import codestacker
    from .args_parser import parse_args
    from .exceptions  import Error
    from .logger      import log_info, log_ko

    # Done outside the global "try-catch", to not mess with argparse inner exceptions handling.
    arguments = parse_args()

    try:
        codestacker.main(arguments)

        log_info('Script stopped')
    except Error as error:
        error.print()
    except KeyboardInterrupt:
        print()
        log_ko('Keyboard interruption: stopping')
    except BaseException:
        traceback.print_exc()

    sys.exit(0)
