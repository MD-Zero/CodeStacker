#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cache building utility--for compilation optimization.
"""

####################################################################################################

def _get_recipe(include, file):
    """
    Return a pair representing a "compilation recipe", i.e. a target and its prerequisites.
    """
    import subprocess

    recipe = None

    try:
        recipe = subprocess.check_output(['g++', '-I', include, '-MM', file])
    except subprocess.CalledProcessError as error:
        pass

    target, prerequisites = recipe.decode('UTF-8').split(':', 1)

    # Remove extra whitespace from the target.
    target = ' '.join(target.split())

    # Remove any backslashes and extra whitespace from the prerequisites.
    prerequisites = prerequisites.replace('\\', '')
    prerequisites = ' '.join(prerequisites.split())

    return {target: prerequisites}
