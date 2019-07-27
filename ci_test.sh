#!/bin/bash
set -e
# working dir
DIR=`dirname "${BASH_SOURCE[0]}"`
cd ${DIR}
# run tests
mkdir -p build
python3 -m coverage run --source=etlx,tests setup.py test
python3 -m coverage report -m --skip-covered > build/coverage.txt
cat build/coverage.txt