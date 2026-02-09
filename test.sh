#!/bin/bash
set -e

if [ "$1" = "base" ]; then
    python -m pytest tests/ -x --ignore=tests/test_map_values.py -q
elif [ "$1" = "new" ]; then
    python -m pytest tests/test_map_values.py -x -q
else
    echo "Usage: ./test.sh [base|new]"
    exit 1
fi
