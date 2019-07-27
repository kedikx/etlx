#!/usr/bin/python3

import os
import setuptools

with open("README.md", "r") as f:
    README = f.read()
with open("VERSION", "r") as f:
    VERSION = f.read()
with open('etlx/build.py','w') as f:
    CI_BUILD_ID = os.environ.get('CI_BUILD_ID',0)
    VERSION += str(CI_BUILD_ID)
    f.write(f"__version__='{VERSION}'\n")

setuptools.setup(
    name="etlx",
    version=VERSION,
    author="Alexander Keda",
    author_email="kedikx.io@gmail.com",
    description="ETL & Co",
    long_description=README,
#    long_description_content_type="text/markdown",
    url="https://github.com/kedikx/etlx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)