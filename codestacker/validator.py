#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML configuration file validator.
"""

ERROR_MESSAGE_1 = 'Missing mandatory key: "{}"'
ERROR_MESSAGE_2 = 'Missing mandatory key in "{}": "{}"'

def validate(config):
    """
    Validate the correctness of a configuration file.
    """
    print(config)

    from .        import keys
    from .helpers import print_and_die

    if isinstance(config, dict):
        config = [config]

    for plan in config:
        if keys.KEY_PROJECT_NAME not in plan:
            print_and_die(ERROR_MESSAGE_1.format(keys.KEY_PROJECT_NAME))

        project_name = plan[keys.KEY_PROJECT_NAME]

        if keys.KEY_PLAN not in plan:
            print_and_die(ERROR_MESSAGE_2.format(project_name, keys.KEY_PLAN))

        if keys.KEY_DIR_INCLUDE not in plan:
            print_and_die(ERROR_MESSAGE_2.format(project_name, keys.KEY_DIR_INCLUDE))

        if keys.KEY_DIR_SOURCE not in plan:
            print_and_die(ERROR_MESSAGE_2.format(project_name, keys.KEY_DIR_SOURCE))
