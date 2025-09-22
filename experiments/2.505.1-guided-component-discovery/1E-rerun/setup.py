#!/usr/bin/env python3
"""
Setup script for JSON Schema Validator CLI Tool
"""

from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="json-schema-validator-cli",
    version="1.0.0",
    description="Professional JSON Schema Validator CLI Tool with External Libraries",
    author="Method 1E External Library Implementation",
    py_modules=["json_validator"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "json-validator=json_validator:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)