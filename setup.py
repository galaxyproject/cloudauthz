"""
Package install information.
"""

import ast
import os
import re

from distutils.core import setup

prog = re.compile(r'__version__\s*=\s*(.+)')
with open(os.path.join('cloud_authz', '__init__.py')) as f:
    for l in f:
        match_object = prog.match(l)
        if match_object:
            version = ast.literal_eval(match_object.group(1))
            break

REQ = [
    'requests == 2.18.4'
]

setup(
    name='cloud-authz',
    version=version,
    description='Implements means of authorization delegation on cloud-based '
                'resource providers without sharing credentials.',
    author='Vahid Jalili',
    url='https://github.com/galaxyproject/cloud-authz',
    install_requires=REQ,
    license='MIT'
)
