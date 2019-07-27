#!/bin/bash
set -e
# working dir
DIR=`dirname "${BASH_SOURCE[0]}"`
cd ${DIR}
# run tests
coverage report -m --skip-covered > coverage.txt
coverage html -d coverage.html
grep "TOTAL" coverage.txt