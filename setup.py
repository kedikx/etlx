#!/usr/bin/python3

import os
from distutils.core import Command
import pkg_resources
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


class Requirements(Command):

    FILENAME = "requirements.txt"

    description = "save project requirements to file"
    user_options = [
        ("filename=", None, f"Output filename (default: {FILENAME})"),
    ]

    def initialize_options(self):
        self.filname = None

    def finalize_options(self):
        if not self.filname:
            self.filname = self.FILENAME

    def run(self):
        requires = []
        install_requires = getattr(self.distribution, "install_requires", [])
        requires.extend(pkg_resources.parse_requirements(install_requires))
        extras_require = getattr(self.distribution, "extras_require", {})
        for extra, reqs in extras_require.items():
            if not extra.startswith(":"):
                continue
            marker = extra[1:]
            e = pkg_resources.invalid_marker(marker)
            if e:
                raise e
            for r in pkg_resources.parse_requirements(reqs):
                assert not r.marker
                r.marker = marker
                requires.append(r)
        with open(self.filname, "w") as f:
            f.write("\n".join(sorted(map(str, requires)))+"\n")


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
    install_requires=["PyYAML"],
    cmdclass={
        "requirements": Requirements,
    },
)
