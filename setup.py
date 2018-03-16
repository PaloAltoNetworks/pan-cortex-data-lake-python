#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Palo Alto Networks Cloud Python SDK setup script."""

from setuptools import setup, find_packages
import socket

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

if hasattr(socket, 'ssl'):
    requirements = [
        'requests',
        'requests-oauthlib',
        'cffi',
        'cryptography'
    ]
else:
    requirements = [
        'requests',
        'requests-oauthlib',
        'pyopenssl',
        'cffi',
        'cryptography'
    ]

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]

setup(
    name='pancloud',
    version='1.0.0',
    description="Python idiomatic SDK for the Palo Alto Networks Application Framework.",
    long_description=readme + '\n\n' + history,
    author="Steven Serrata",
    author_email='sserrata@paloaltonetworks.com',
    url='https://github.com/PaloAltoNetworks/pancloud',
    packages=find_packages(include=['pancloud']),
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='pancloud',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
