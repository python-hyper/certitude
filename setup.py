#!/usr/bin/env python
from setuptools import setup, find_packages

long_description = (
    open("README.rst").read()
)


setup(
    name="certitude",
    version="0.0.1",

    description="A library that provides access to system certificate stores.",
    long_description=open("README.rst").read(),
    url="https://github.com/python-hyper/certitude/",
    license="MIT",

    author="Cory Benfield",
    author_email="cory@lukasa.co.uk",

    install_requires=[
        "cryptography>=1.1.2,<2.0",
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},

    classifiers=[
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
