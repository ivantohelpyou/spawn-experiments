"""Setup script for URL Validator package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="url-validator",
    version="1.0.0",
    author="URL Validator Project",
    author_email="contact@urlvalidator.com",
    description="A comprehensive URL validation library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urlvalidator/url-validator",
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
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=[req for req in requirements if not any(dev in req for dev in ["pytest", "black", "mypy", "flake8", "sphinx"])],
    extras_require={
        "dev": requirements,
        "test": [req for req in requirements if "pytest" in req or "responses" in req],
    },
    entry_points={
        "console_scripts": [
            "url-validator=url_validator.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)