#!/usr/bin/env python

from setuptools import setup, find_packages
import os


def extra_dependencies():
    import sys
    ret = []
    if sys.version_info < (2, 7):
        ret.append('argparse')
    return ret


def read(*names):
    values = dict()
    extensions = ['.txt', '.rst']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='py_mt_strategy_runner',
    #version=TODO.__version__,
    description='Test MT4 strategy',
    long_description=long_description,
    classifiers=[
        "Development Status :: testing",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation",
    ],
    keywords='run test configurations of MT4 strategy and send results to storage',
    author='Ihar Malkevich',
    author_email='imalkevich@gmail.com',
    maintainer='Ihar Malkevich',
    maintainer_email='imalkevich@gmail.com',
    url='https://github.com/imalkevich/py_mt_strategy_runner',
    license='TODO',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'TODO',
        ]
    },
    install_requires=[
        'keras',
        'numpy',
        'PTable',
        'pandas',
        'pyodbc',
        'pyquery',
        'tensorflow'
    ] + extra_dependencies(),
    test_require = ['coverage', 'codecov']
)
