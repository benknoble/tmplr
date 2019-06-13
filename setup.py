#! /usr/bin/env python

from setuptools import setup
import io

import tmplr


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


setup(
    name='tmplr',
    version=tmplr.__version__,
    url='https://github.com/benknoble/tmplr',
    author='D. Ben Knoble',
    author_email='ben.knoble@gmail.com',
    license='MIT',
    description='The holiest cli template system',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],
    install_requires=[
        ],
    python_requires='>=3',
    packages=[
        'tmplr',
        'tmplr_cli',
        ],
    test_suite='tests.suite',
    entry_points={
        'console_scripts': [
            'tmplr=tmplr_cli.tmplr_app:main',
            'temples=tmplr_cli.temples_app:main',
            ],
    },
)
