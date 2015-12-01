#!/usr/bin/env python

from setuptools import setup, find_packages

__author__ = 'Eugenio Marinetto'

setup(
    name='pyimagej',
    version="1.0.7",
    packages=find_packages(),
    install_requires=['ctk_cli'],
    author='Eugenio Marinetto',
    author_email='marinetto@jhu.edu',
    description='Python Toolkit for ImageJ Macro calling from python code',
    url='http://github.com/nenetto/pyimagej',
    dependency_links = ['http://github.com/nenetto/ctk-cli']
)
