#!/usr/bin/env python

import sys

from setuptools import setup, find_packages


tests_require = []

if sys.version_info.major == 2:
    tests_require.append("unittest2")


setup(
    name='richenum',
    version='1.2.0',
    description='Enum library for python.',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read() + '\n\n' +
        open('AUTHORS.rst').read()),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='python enum richenum',
    url='https://github.com/hearsaycorp/richenum',
    author='Hearsay Social',
    author_email='opensource@hearsaysocial.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    tests_require=tests_require,
    install_requires=['six'],
    test_suite='tests'
)
