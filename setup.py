#!/usr/bin/python3

import os
import setuptools

BASEDIR = os.path.dirname(__file__)

with open(os.path.join(BASEDIR, "README.md"), "r") as f:
    README = f.read()
with open(os.path.join(BASEDIR, "VERSION"), "r") as f:
    VERSION = f.read().strip()
with open(os.path.join(BASEDIR, "etlx", "build.py"), "w") as f:
    GITHUB_WORKFLOW = os.environ.get("GITHUB_WORKFLOW")
    if GITHUB_WORKFLOW == "etlx-release":
        pass
    elif GITHUB_WORKFLOW == "etlx-build":
        GITHUB_RUN_NUMBER = os.environ.get("GITHUB_RUN_NUMBER")
        VERSION += f".dev{GITHUB_RUN_NUMBER}"
    else:
        CI_BUILD_ID = os.environ.get("CI_BUILD_ID", 0)
        VERSION += f".dev{CI_BUILD_ID}"
    f.write(f'__version__ = "{VERSION}"\n')

setuptools.setup(
    name="etlx",
    version=VERSION,
    author="Alexander Keda",
    author_email="kedikx.io@gmail.com",
    description="ETL & Co",
    long_description=README,
    # long_description_content_type="text/markdown",
    url="https://github.com/kedikx/etlx",
    packages=setuptools.find_packages(exclude=("etlx_tests", "etlx_tests.*")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "PyYAML"
        ],
)
