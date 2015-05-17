# -*- coding: utf-8 -*-

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('ynab/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='pynab',
    author='Ivan Smirnov',
    author_email='i.s.smirnov@gmail.com',
    version=version,
    url='http://github.com/aldanor/pynab',
    packages=['ynab'],
    description='A minimalistic library designed to make it easy to access YNAB data from Python.',
    install_requires=[
        'six',
        'toolz',
        'enum34',
        'schematics',
        'dateparser'
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
