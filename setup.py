#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script.
"""

from setuptools import setup

import codestacker

setup(
    name=codestacker.__name__,
    version=codestacker.__version__,
    description=codestacker.__doc__,
    url='https://github.com/MD-Zero/CodeStacker',
    author='Matthieu Dufour',
    author_email='mdufourpro@gmail.com',
    license='MIT',
    packages=['codestacker'],
    install_requires=['PyYAML'],
    scripts=['scripts/codestacker']
)
