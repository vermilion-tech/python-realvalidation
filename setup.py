#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['pbr', 'setuptools_scm'],
    pbr=True,
    use_scm_version={'local_scheme': 'node-and-timestamp'}
)
