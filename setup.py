"""
Package install information.
"""

import ast
import re

from setuptools import setup, find_packages
from os import path

current_directory = path.abspath(path.dirname(__file__))

with open(path.join(current_directory, 'README.md')) as f:
    long_description = f.read()

prog = re.compile(r'__version__\s*=\s*(.+)')
with open(path.join(current_directory, 'cloudauthz', '__init__.py')) as f:
    for l in f:
        match_object = prog.match(l)
        if match_object:
            version = ast.literal_eval(match_object.group(1))
            break

REQ = [
    'requests >= 2.18.4',
    'adal >= 1.0.2'
]

setup(
    name='cloudauthz',
    version=version,
    description='Implements means of authorization delegation on cloud-based resource providers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Vahid Jalili',
    author_email='jalili.vahid@gmail.com',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    url='https://github.com/galaxyproject/cloudauthz',
    install_requires=REQ,
    license='MIT',
    keywords='Cloud Authorization Access',
)
