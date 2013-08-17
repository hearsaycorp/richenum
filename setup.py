#!/usr/bin/env python

from setuptools import setup, find_packages


tests_require = [
    'unittest2',
]


setup(
    name='richenum',
    version='1.0.0',
    description='Enum library for python.',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGELOG.rst').read() + '\n\n' +
        open('AUTHORS.rst').read()),
    classifiers=[],
    keywords='python enum richenum',
    url='https://github.com/hearsaycorp/richenum',
    author='Hearsay Social',
    author_email='opensource@hearsaysocial.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    tests_require=tests_require,
    test_suite='tests'
)
