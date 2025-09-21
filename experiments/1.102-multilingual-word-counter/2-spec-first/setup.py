"""
Setup script for the Multilingual Word Counter application.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="multilingual-word-counter",
    version="1.0.0",
    author="Multilingual Word Counter Team",
    author_email="contact@example.com",
    description="A comprehensive tool for counting words in multiple languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/multilingual-word-counter",
    py_modules=[
        "multilingual_word_counter",
        "models",
        "language_detector",
        "word_counter",
        "text_analyzer",
        "input_handler",
        "output_formatter"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langdetect>=1.0.9",
        "nltk>=3.8",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
    ],
    extras_require={
        "full": [
            "spacy>=3.4.0",
            "jieba>=0.42.1",
            "python-docx>=0.8.11",
            "PyPDF2>=3.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
    },
    entry_points={
        "console_scripts": [
            "mwc=multilingual_word_counter:main",
            "multilingual-word-counter=multilingual_word_counter:main",
        ],
    },
    keywords="multilingual word count text analysis language detection nlp",
    project_urls={
        "Bug Reports": "https://github.com/example/multilingual-word-counter/issues",
        "Documentation": "https://github.com/example/multilingual-word-counter#readme",
        "Source": "https://github.com/example/multilingual-word-counter",
    },
)