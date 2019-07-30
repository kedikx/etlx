#!/bin/bash
set -e
# working dir
DIR=`dirname "${BASH_SOURCE[0]}"`
cd ${DIR}
# run tests
coverage run setup.py test
