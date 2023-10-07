#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))
from ansibledocgen import __version__, __author__

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

try:
    from setuptools import setup, find_packages
except ImportError:
    print("ansible-docgen needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

setup(
    name='ansible-docgen',
    version=__version__,
    description='Generate Documentation from Annotated Ansible Playbooks and Roles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=__author__,
    author_email='david@davidwhiteside.com',
    url='https://github.com/starboarder2001/ansible-docgen',
    license='MIT',
    install_requires=[
        'PyYAML',
        'setuptools',
	'jinja2'],
    include_package_data=True,
    package_dir={
        '': 'lib'},
    package_data = { '': ['*.j2']},
    packages=find_packages('lib'),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
          'ansible-docgen = ansibledocgen.cli:main'
        ]
    },
    data_files=[],
)
