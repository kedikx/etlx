#!/bin/bash
set -e
# working dir
DIR=`dirname "${BASH_SOURCE[0]}"`
cd ${DIR}
# run tests
coverage run --source=etlx,tests setup.py test
