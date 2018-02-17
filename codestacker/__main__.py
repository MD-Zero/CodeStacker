#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script's main entry point.
"""

if __name__ == '__main__':
    import sys
    import traceback

    from .           import codestacker
    from .exceptions import Error
    from .logger     import log_error, log_info, log_ko

    try:
        codestacker.main()

        log_info('Script stopped')
    except Error as error:
        error.print()
    except KeyboardInterrupt:
        print()
        log_ko('Keyboard interruption: stopping')
    except BaseException:
        traceback.print_exc()

    sys.exit(0)
