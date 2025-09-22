#!/usr/bin/env python3
"""Setup configuration for JSON Schema Validator CLI."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jsv-cli",
    version="1.0.0",
    author="CLI Developer",
    author_email="dev@example.com",
    description="A command-line JSON Schema Validator tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "jsonschema>=4.0.0",
        "click>=8.0.0",
        "colorama>=0.4.0",
        "tqdm>=4.60.0",
    ],
    entry_points={
        "console_scripts": [
            "jsv=jsv.cli:main",
        ],
    },
)