#!/usr/bin/python3
# python3 setup.py sdist; twine upload dist/*
from setuptools import setup

with open("README", "r") as file:
    desc = file.read()

setup(
    name             = "ccash_python_client",
    packages         = ["ccash_python_client"],
    version          = "1.0.0",
    license          = "MIT",
    description      = "Python client for CCash servers",
    long_description = desc,
    long_description_content_type = "text/plain",
    author           = "FearlessDoggo21",
    author_email     = "fearlessdoggo21@vivaldi.net",

    install_requires = [
        "requests"
    ],

    classifiers      = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
)
