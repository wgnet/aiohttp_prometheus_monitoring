#!/usr/bin/env python

import os

from setuptools import setup, find_packages


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(ROOT_DIR, 'VERSION')
BUILD_NUMBER = os.environ.get('BUILD_NUMBER')


def read_file(file_path):
    return open(file_path).read().strip()


__version__ = read_file(os.path.join(ROOT_DIR, 'VERSION'))


if BUILD_NUMBER:
    full_version = '%s.%s' % (__version__, BUILD_NUMBER)
    f = open(VERSION_FILE, 'w')
    try:
        f.writelines([full_version])
    finally:
        f.close()


setup(
    name='aiohttp_prometheus_monitoring',
    version=read_file(os.path.join(ROOT_DIR, 'VERSION')),
    packages=find_packages(),
    long_description=read_file(os.path.join(ROOT_DIR, 'README.md')),
    include_package_data=True,
    author='Wargaming Team',
    install_requires=[
        'aiohttp',
        'prometheus_client>=0.0.21',
        'prometheus-async>=17.4.0',
    ],
    extras_require={
        'amqp': ['aioamqp>=0.9.0'],
        'postgres': ['aiopg'],
        'redis': ['aioredis'],
        'mysql': ['aiomysql'],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
