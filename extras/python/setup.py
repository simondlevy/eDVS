#!/usr/bin/env python3

'''
Python distutils setup file for eDVS module.

Copyright (C) 2020 Simon D. Levy

MIT License
'''

#from distutils.core import setup
from setuptools import setup

setup (name = 'edvs',
    version = '0.1',
    install_requires = ['numpy'],
    description = 'Python class for iniVation eDVS',
    packages = ['edvs'],
    author='Simon D. Levy',
    author_email='simon.d.levy@gmail.com',
    url='https://github.com/simondlevy/eDVS',
    license='MIT',
    platforms='Linux; Windows; OS X'
    )
