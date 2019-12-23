#!/usr/bin/env python
"""revelation setup file"""

import os
import re

from setuptools import find_packages, setup

PACKAGE = "revelation"
REQUIREMENTS = [
    "Jinja2==2.10.3",
    "Werkzeug==0.16.0",
    "click==7.0",
    "gevent-websocket==0.10.1",
    "gevent==1.4.0",
    "watchdog==0.9.0",
]
TEST_REQUIREMENTS = [
    "coverage==4.5.4",
    "coveralls==1.9.2",
    "flake8==3.7.9",
    "mock==3.0.5",
    "nose==1.3.7",
]

with open("README.md", "r") as f:
    README = f.read()

with open(os.path.join(PACKAGE, "__init__.py")) as init_file:
    INIT = init_file.read()

VERSION = re.search(
    "^__version__ = ['\"]([^'\"]+)['\"]", INIT, re.MULTILINE
).group(1)
AUTHOR = re.search(
    "^__author__ = ['\"]([^'\"]+)['\"]", INIT, re.MULTILINE
).group(1)
EMAIL = re.search(
    "^__email__ = ['\"]([^'\"]+)['\"]", INIT, re.MULTILINE
).group(1)

setup(
    name=PACKAGE,
    version=VERSION,
    description="Make awesome reveal.js presentations with revelation",
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url="https://github.com/humrochagf/revelation",
    license="MIT",
    packages=find_packages(),
    package_data={PACKAGE: ["templates/presentation.html"]},
    zip_safe=False,
    install_requires=REQUIREMENTS,
    entry_points=dict(console_scripts=["revelation=revelation.cli:cli"]),
    platforms="any",
    keywords="presentation slides reveal.js markdown",
    classifiers=[
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    test_suite="tests",
    tests_require=TEST_REQUIREMENTS,
    extras_require={"test": TEST_REQUIREMENTS},
)
