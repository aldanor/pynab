# -*- coding: utf-8 -*-

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pynab/_version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='pynab',
    author='Ivan Smirnov',
    author_email='i.s.smirnov@gmail.com',
    version=version,
    url='http://github.com/aldanor/pynab',
    packages=['ynab'],
    description='A simple API providing native Python access to YNAB data.',
    install_requires=[
        'six',
        'py',
        'toolz',
        'enum34',
        'schematics'
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
