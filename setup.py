#!/usr/bin/env python
import os.path

from setuptools import setup, find_packages

from rust_ext import build_rust_cmdclass, install_lib_including_rust

long_description = (
    open("README.rst").read()
)

setup(
    name="certitude",
    version="1.0.0",

    description="A library that provides access to system certificate stores.",
    long_description=open("README.rst").read(),
    url="https://github.com/python-hyper/certitude/",
    license="MIT",

    author="Cory Benfield",
    author_email="cory@lukasa.co.uk",

    setup_requires=[
        "cffi>=1.0.0",
    ],
    install_requires=[
        "cffi>=1.0.0",
    ],

    cffi_modules=["src/certitude/build.py:ffi"],

    packages=find_packages('src'),
    package_dir={'': 'src'},

    cmdclass={
        "build_rust": build_rust_cmdclass(
            os.path.join("src", "rust-certitude", "c-certitude", "Cargo.toml")
        ),
        "install_lib": install_lib_including_rust,
    },
    ext_package="certitude",

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
