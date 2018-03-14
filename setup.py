#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script.
"""

from setuptools import find_packages, setup

import codestacker

setup(
    name=codestacker.__name__,
    version=codestacker.__version__,
    description=codestacker.__doc__,
    url='https://github.com/MD-Zero/CodeStacker',
    author='Matthieu Dufour',
    author_email='mdufourpro@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['*.tests']),
    install_requires=['PyYAML'],
    include_package_data=True,
    scripts=['scripts/codestacker'],
    test_suite='nose.collector',
    tests_require=['nose']
)
