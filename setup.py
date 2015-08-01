#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))

try:
    from setuptools import setup, find_packages
except ImportError:
    print("ansible-docgen needs setuptools in order to build. Install it using"
            " your package manager (usually python-setuptools) or via pip (pip"
            " install setuptools).")
    sys.exit(1)

setup(name='ansible-docgen',
      version="0.0.1",
      description='Generate Documentation from Annotated Ansible Playbooks and Roles',
      author="David Whiteside",
      author_email='david@davidwhiteside.com',
      url='http://www.davidwhiteside.com/',
      license='MIT',
      install_requires=["PyYAML", 'setuptools'],
      package_dir={ '': 'lib' },
      packages=find_packages('lib'),
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Installation/Setup',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',
      ],
      scripts=[
         'bin/ansible-docgen',
      ],
      data_files=[],
)