#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Palo Alto Networks Cloud Python SDK setup script."""

from setuptools import setup, find_packages
import re

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    regex = re.compile(r"(.+==[0-9]+\.[0-9]+\.[0-9]+)")
    requirements = regex.findall(requirements_file.read())

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    name="pan-cortex-data-lake",
    version="2.0.0-a7",
    description="Python idiomatic SDK for Cortex™ Data Lake.",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Steven Serrata",
    author_email="sserrata@paloaltonetworks.com",
    url="https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python",
    packages=find_packages(
        include=["pan_cortex_data_lake", "pan_cortex_data_lake.adapters"]
    ),
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords="cortex data lake",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite="tests",
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
